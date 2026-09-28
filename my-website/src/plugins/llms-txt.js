// Post-build SEO/LLM helpers (no dependencies):
//   - build/llms.txt       curated index of components + API references (llmstxt.org format)
//   - build/llms-full.txt  every component doc as plain markdown, for LLM ingestion
//   - adds <meta name="robots" content="noindex"> to the sample/template pages so
//     they stay browsable for contributors but out of search results.
// Everything is derived from the docs on disk (category labels/descriptions written
// by seo_meta.py) and the built category pages, so nothing is maintained by hand.

const fs = require('fs');
const path = require('path');

// Built-output folders (relative to outDir) that are templates, not real content.
const NOINDEX_PATHS = ['sample_docs', path.join('api', 'Sample APIs'), path.join('api', 'tags', 'sample-api.html')];
const SKIP_API = new Set(['Sample APIs']);
const SECTIONS = [
  ['Education', 'Education/intro', 'Curricula and learning material for youth and professionals.'],
  ['Workshops', 'workshops/intro', 'Workshop materials and recordings.'],
  ['Resources', 'other_resources/intro', 'Hosted ICICLE services and other resources.'],
  ['Documentation tags', 'docs/tags', 'Browse components by thrust and release (e.g. "Release 2026-09").'],
];

const readJson = (p) => {
  try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return null; }
};

const stripFrontmatter = (text) => text.replace(/^---\n[\s\S]*?\n---\n/, '');

const frontmatterValue = (text, key) => {
  const m = text.match(new RegExp(`^${key}:\\s*(.+)$`, 'm'));
  if (!m) return null;
  const v = m[1].trim();
  try { return JSON.parse(v); } catch { return v.replace(/^['"]|['"]$/g, ''); }
};

// Map category label -> canonical slug by reading the built generated-index pages;
// the base slug (no "-1"/"-2" suffix) wins, matching the catalog's links.
function categorySlugs(outDir) {
  const dir = path.join(outDir, 'docs', 'category');
  const slugs = {};
  if (!fs.existsSync(dir)) return slugs;
  for (const file of fs.readdirSync(dir).sort()) {
    if (!file.endsWith('.html')) continue;
    const slug = file.slice(0, -5);
    const html = fs.readFileSync(path.join(dir, file), 'utf8');
    const m = html.match(/<title[^>]*>([^<|]+?)\s*\|/);
    if (!m) continue;
    const label = m[1].replace(/&amp;/g, '&').trim();
    if (!slugs[label] || !/-\d+$/.test(slug)) slugs[label] = slug;
  }
  return slugs;
}

function addNoindex(dir) {
  if (!fs.existsSync(dir)) return 0;
  if (fs.statSync(dir).isFile()) return markNoindex(dir);
  let n = 0;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) n += addNoindex(p);
    else if (entry.name.endsWith('.html')) n += markNoindex(p);
  }
  return n;
}

function markNoindex(file) {
  const html = fs.readFileSync(file, 'utf8');
  if (html.includes('name="robots"')) return 0;
  fs.writeFileSync(file, html.replace('<head>', '<head><meta name="robots" content="noindex, follow">'));
  return 1;
}

module.exports = function llmsTxtPlugin(context) {
  return {
    name: 'llms-txt',
    async postBuild({ outDir }) {
      const { siteDir, siteConfig } = context;
      const site = siteConfig.url.replace(/\/$/, '') + siteConfig.baseUrl.replace(/\/$/, '');
      const url = (route) => `${site}/${route.split('/').map(encodeURIComponent).join('/')}`;
      const slugs = categorySlugs(outDir);

      // Components (docs/<Folder>/)
      const docsDir = path.join(siteDir, 'docs');
      const components = [];
      for (const folder of fs.readdirSync(docsDir).sort((a, b) => a.localeCompare(b))) {
        const cat = readJson(path.join(docsDir, folder, '_category_.json'));
        if (!cat) continue;
        const label = cat.label || folder;
        const slug = slugs[label];
        components.push({
          folder, label,
          link: slug ? url(`docs/category/${slug}`) : url(`docs/${folder}`),
          description: (cat.link && cat.link.description) || '',
        });
      }

      // API references (api-docs/<Folder>/*.info.mdx)
      const apiDir = path.join(siteDir, 'api-docs');
      const apis = [];
      for (const folder of fs.readdirSync(apiDir).sort()) {
        if (SKIP_API.has(folder)) continue;
        const d = path.join(apiDir, folder);
        if (!fs.statSync(d).isDirectory()) continue;
        const info = fs.readdirSync(d).find((f) => f.endsWith('.info.mdx'));
        if (!info) continue;
        const text = fs.readFileSync(path.join(d, info), 'utf8');
        // gen-api-docs keeps only the spec description's first line, so prefer the
        // component's own doc description when the API has a matching doc folder.
        const doc = components.find((c) => c.label === folder || c.folder === folder);
        apis.push({
          label: folder,
          link: url(`api/${folder}/${info.replace(/\.info\.mdx$/, '')}`),
          description: (doc && doc.description) || frontmatterValue(text, 'description') || '',
        });
      }

      const line = (x) => `- [${x.label}](${x.link})${x.description ? `: ${x.description}` : ''}`;
      const llms = [
        `# ${siteConfig.title}`,
        '',
        `> ${siteConfig.customFields.siteDescription}`,
        '',
        'Each component page links its Tutorials, How-To Guides and Explanation. Components are tagged by ICICLE thrust (CI4AI, AI4CI, Software, Foundation-AI, Digital-Agriculture, Animal-Ecology, Smart-Foodsheds, Food-Access) and by release ("Release YYYY-MM").',
        `Full text of every component doc: ${site}/llms-full.txt`,
        '',
        '## Components',
        '',
        ...components.map(line),
        '',
        '## API References',
        '',
        ...apis.map(line),
        '',
        '## Optional',
        '',
        ...SECTIONS.map(([label, route, description]) => line({ label, link: url(route), description })),
        '',
      ].join('\n');
      fs.writeFileSync(path.join(outDir, 'llms.txt'), llms);

      // Full text: main page first, then the section pages, frontmatter stripped.
      const order = (f, folder) => (f.toLowerCase().startsWith(folder.toLowerCase() + '.') ? 0 : 1);
      const full = [`# ${siteConfig.title}`, '', `> ${siteConfig.customFields.siteDescription}`, ''];
      for (const c of components) {
        const dir = path.join(docsDir, c.folder);
        const files = fs.readdirSync(dir)
          .filter((f) => /\.mdx?$/.test(f))
          .sort((a, b) => order(a, c.folder) - order(b, c.folder) || a.localeCompare(b));
        full.push(`\n\n# ${c.label}\n\nSource: ${c.link}\n`);
        for (const f of files) {
          full.push(stripFrontmatter(fs.readFileSync(path.join(dir, f), 'utf8')).trim(), '');
        }
      }
      fs.writeFileSync(path.join(outDir, 'llms-full.txt'), full.join('\n'));

      const hidden = NOINDEX_PATHS.reduce((n, d) => n + addNoindex(path.join(outDir, d)), 0);
      console.log(`[llms-txt] ${components.length} components, ${apis.length} APIs; noindex on ${hidden} template page(s)`);
    },
  };
};
