import { themes as prismThemes } from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config = {
  title: 'ICICLE AI Institute - Training Catalog',
  tagline: 'Documentation and APIs of ICICLE AI Institute projects.',
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
        docs: false,
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
      '@docusaurus/plugin-content-docs',
      {
        id: 'docs',
        path: 'docs', // this is where all the folder containning .md files are present
        sidebarPath: './sidebars.js',
        routeBasePath: 'docs', // thie is for the url
        // docItemComponent: '@theme/ApiItem',  //Not needed for normal docs
        tagsBasePath: 'tags'
      },
  
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'api',                // plugin ID (must be unique)
        path: 'api-docs',         // folder with .mdx for API docs
        routeBasePath: 'api',     // for the url
        sidebarPath: './sidebars.js',
        docItemComponent: '@theme/ApiItem', 
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'curriculum',
        path: 'curriculum', // this is where all the folder containning .md files are present
        sidebarPath: './sidebars.js',
        routeBasePath: 'curriculum', // thie is for the url
        tagsBasePath: 'tags'
      },
  
    ],

    [
      'docusaurus-plugin-openapi-docs',
      {
        id: 'openapi', // Plugin ID
        docsPluginId: 'api', // Associate it with API docs
        config: {
          sample_1: {
            specPath: 'api_config_files/sample_1.yaml', // Path to OpenAPI spec
            outputDir: 'api-docs/Project-1 APIs', // API docs location
            sidebarOptions: {
              groupPathsBy: "tag",
            },
          },
          sample_2: {
            specPath: 'api_config_files/sample_2.json', // Path to OpenAPI spec
            outputDir: 'api-docs/Project-2 APIs', // API docs location
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
      title: 'ICICLE AI Training Catalog',
      logo: {
        alt: 'My Site Logo',
        src: 'img/ICICLE_logo.jpg',
      },
      items: [
        { to: '/training-catalog/docs/intro', label: 'Documentation', position: 'left' },
        { to: '/training-catalog/api/intro', label: 'APIs', position: 'left' }, // API Docs
        { to: '/training-catalog/curriculum/intro', label: 'Curriculum', position: 'left' }, // Curriculum Docs
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Copyright © ${new Date().getFullYear()} National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606). Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },
};

module.exports = config;
