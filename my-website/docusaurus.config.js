import { themes as prismThemes } from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config = {
  title: 'ICICLE Training Catalog',
  tagline: 'Training and APIs documentation.',
  favicon: 'img/favicon.ico',

  // // Set the production url of your site here
  // url: 'https://your-docusaurus-site.example.com',
  // // Set the /<baseUrl>/ pathname under which your site is served
  // // For GitHub pages deployment, it is often '/<projectName>/'
  // baseUrl: '/',


  url: 'https://ICICLE-ai.github.io', // Your GitHub Pages root
  baseUrl: '/training-catalog/', // The repository name, with a trailing slash
  organizationName: 'ICICLE-ai', // Your GitHub organization name
  projectName: 'training-catalog', // Your GitHub repository name
  deploymentBranch: 'gh-pages', // This is where GitHub Pages will be deployed
  trailingSlash: false, // Helps with correct URL resolution


  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'facebook', // Usually your GitHub org/user name.
  projectName: 'docusaurus', // Usually your repo name.

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  scripts: [
    {
      src: 'https://umami.pods.icicleai.tapis.io/script.js', //Correct Umami tracking script URL
      async: true,
      defer: true,
      'data-website-id': '0502dde3-2e0b-4a95-83b0-407cfa13ee91', //  Umami website ID
    },
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.js',
          docItemComponent: "@theme/ApiItem",
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        // blog: {
        //   showReadingTime: true,
        //   feedOptions: {
        //     type: ['rss', 'atom'],
        //     xslt: true,
        //   },
        //   editUrl:
        //     'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        //   onInlineTags: 'warn',
        //   onInlineAuthors: 'warn',
        //   onUntruncatedBlogPosts: 'warn',
        // },
        theme: {
          customCss: './src/css/custom.css',
        },
      },
    ],
  ],

  themes: [
    'docusaurus-theme-openapi-docs',
  ],

  plugins: [
    [
      'docusaurus-plugin-openapi-docs',
      {
        id: 'api', // Plugin id
        docsPluginId: 'classic', // Configured for preset-classic
        config: {
          patra: {
            specPath: 'examples/patra.yaml',
            outputDir: 'docs/patra',
            sidebarOptions: {
              groupPathsBy: "tag",
            },
          },
        },
      },
    ],
    [
      "@dipakparmar/docusaurus-plugin-umami",
        /** @type {import('@dipakparmar/docusaurus-plugin-umami').Options} */
        ({
          websiteID: "0502dde3-2e0b-4a95-83b0-407cfa13ee91", // Required
          analyticsDomain: "icicle-ai.github.io", // Required
          dataHostURL: "https://umami.pods.icicleai.tapis.io", // Optional
          dataAutoTrack: true, // Optional
          dataDoNotTrack: false, // Optional
          dataCache: true, // Optional
          dataDomains: "icicle-ai.github.io", // comma separated list of domains, *Recommended*
        }),
    ],
  ],

  themeConfig: {
    image: 'img/ICICLE_logo.jpg',
    navbar: {
      title: 'ICICLE Training Catalog',
      logo: {
        alt: 'My Site Logo',
        src: 'img/ICICLE_logo.jpg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Tutorial',
        },
        // { to: '/blog', label: 'Blog', position: 'left' },
        {
          href: 'https://github.com/facebook/docusaurus',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Tutorial',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/docusaurus',
            },
            {
              label: 'Discord',
              href: 'https://discordapp.com/invite/docusaurus',
            },
            {
              label: 'X',
              href: 'https://x.com/docusaurus',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/facebook/docusaurus',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} ICICLE AI Institute. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },
};

module.exports = config;
