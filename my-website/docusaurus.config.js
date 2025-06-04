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
      'data-website-id': 'e1e727a2-edd2-436d-a3f0-3794e11d3718', //  Umami website ID
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
        routeBasePath: 'docs', // this is for the url
        // docItemComponent: '@theme/ApiItem',  //Not needed for normal docs
        tagsBasePath: 'tags',
        showLastUpdateTime: true,
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
        showLastUpdateTime: true,
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'Education',
        path: 'Education', // this is where all the folder containning .md files are present
        sidebarPath: './sidebars.js',
        routeBasePath: 'Education', // this is for the url
        tagsBasePath: 'tags',
        showLastUpdateTime: true,
      },
  
    ],

    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'workshops',
        path: 'workshops', // this is where all the folder containning .md files are present
        sidebarPath: './sidebars.js',
        routeBasePath: 'workshops', // this is for the url
        tagsBasePath: 'tags',
        showLastUpdateTime: true,
      },
  
    ],

    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'sample_docs',
        path: 'sample_docs', // this is where all the folder containning .md files are present
        sidebarPath: './sidebars.js',
        routeBasePath: 'sample_docs', // this is for the url
        tagsBasePath: 'tags',
        showLastUpdateTime: true,
      },
  
    ],

    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'other_resources',
        path: 'other_resources', // this is where all the folder containning .md files are present
        sidebarPath: './sidebars.js',
        routeBasePath: 'other_resources', // this is for the url
        tagsBasePath: 'tags',
        showLastUpdateTime: true,
      },
  
    ],

    [
      'docusaurus-plugin-openapi-docs',
      {
        id: 'openapi', // Plugin ID
        docsPluginId: 'api', // Associate it with API docs
        config: {
          sample_2: {
            specPath: 'api_config_files/sample_apis.json', // Path to OpenAPI spec
            outputDir: 'api-docs/Sample APIs', // API docs location
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
          websiteID: "e1e727a2-edd2-436d-a3f0-3794e11d3718", // Required
          analyticsDomain: "icicle-ai.github.io", // Required
          dataHostURL: "https://umami.pods.icicleai.tapis.io", //Required
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
      title: 'ICICLE AI Institute Training Catalog',
      logo: {
        alt: 'My Site Logo',
        src: 'img/ICICLE_logo.jpg',
      },
      items: [
        { to: '/training-catalog/docs/intro', label: 'Documentation', position: 'left' },
        { to: '/training-catalog/api/intro', label: 'APIs', position: 'left' }, // API Docs
        { to: '/training-catalog/Education/intro', label: 'Education', position: 'left' }, // Education 
        { to: '/training-catalog/other_resources/intro', label: 'Resources', position: 'left' }, 
        { to: '/training-catalog/workshops/intro', label: 'Workshops', position: 'left' },   
        { to: '/training-catalog/sample_docs/intro', label: 'Sample Documentation', position: 'left' },
        { to: '/training-catalog/docs/tags', label: 'Tags',  position: 'left' },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `© ${new Date().getFullYear()} National Science Foundation (NSF) funded AI institute for Intelligent Cyberinfrastructure with Computational Learning in the Environment (ICICLE) (OAC 2112606). Learn more about <a href="https://icicle.ai/" target="_blank" rel="noopener noreferrer">ICICLE AI Institute.</a>`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },
};

module.exports = config;
