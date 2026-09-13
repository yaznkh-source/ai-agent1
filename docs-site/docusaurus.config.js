// @ts-check
// Docusaurus config - AI Agency OS - 68 agents, 292 skills

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI Agency OS',
  tagline: 'Private AI Agency System - 68 Agents, 292 Skills - ECC + Open WebUI Inspired',
  favicon: 'img/favicon.ico',

  url: 'https://docs.ai-agency.os',
  baseUrl: '/',

  organizationName: 'ai-agency-os',
  projectName: 'ai-agency-os-docs',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ar'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          editUrl: 'https://github.com/yaznkh-source/ai-agent1/tree/arena/01a09ae9-ai-agent1/docs/',
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/yaznkh-source/ai-agent1/tree/arena/01a09ae9-ai-agent1/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/social-card.png',
      navbar: {
        title: 'AI Agency OS',
        logo: {
          alt: 'AI Agency OS Logo - 68 Agents 292 Skills',
          src: 'img/logo.svg',
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Docs',
          },
          { to: '/blog', label: 'Blog', position: 'left' },
          { to: '/pricing', label: 'Pricing $0/$49/$199/$999', position: 'left' },
          {
            href: 'https://github.com/yaznkh-source/ai-agent1',
            label: 'GitHub 68⭐292',
            position: 'right',
          },
          {
            href: 'https://8000-ie7q8eouxddcow66c2bgs.e2b.app/api/docs',
            label: 'API Docs',
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
              { label: 'Quickstart 5min', to: '/docs/quickstart' },
              { label: 'Architecture 68/292', to: '/docs/architecture' },
              { label: 'API 18 Routers', to: '/docs/api' },
              { label: 'Agents 68', to: '/docs/agents/overview' },
              { label: 'Skills 292', to: '/docs/skills/overview' },
            ],
          },
          {
            title: 'SaaS',
            items: [
              { label: 'Billing Stripe', to: '/docs/saas/billing' },
              { label: 'White-label $199/$499/$999', to: '/docs/production/white-label' },
              { label: 'Marketplace 30%', to: '/docs/saas/marketplace' },
              { label: 'Teams RBAC', to: '/docs/saas/teams' },
            ],
          },
          {
            title: 'Production',
            items: [
              { label: 'Docker Prod', to: '/docs/production/deployment' },
              { label: 'K8s 3+2 Replicas', to: '/docs/production/k8s' },
              { label: 'Security SOC2/GDPR', to: '/docs/production/security' },
              { label: 'Realtime WS', to: '/docs/production/realtime' },
              { label: 'Zapier 5000+ Apps', to: '/docs/integrations/zapier' },
            ],
          },
          {
            title: 'More',
            items: [
              { label: 'Blog', to: '/blog' },
              { label: 'GitHub', href: 'https://github.com/yaznkh-source/ai-agent1' },
              { label: 'Live Demo 22 Views', href: 'https://5173-ie7q8eouxddcow66c2bgs.e2b.app' },
              { label: 'Business Plan $150K MRR', to: '/docs/business/business-plan' },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} AI Agency OS - 68 Agents, 292 Skills, 19 Routers, 22 Views, Built with ECC + Open WebUI.`,
      },
      prism: {
        theme: require('prism-react-renderer').themes.github,
        darkTheme: require('prism-react-renderer').themes.dracula,
      },
      algolia: {
        appId: 'AIAGENCYOS',
        apiKey: 'aiagencyos-search-key',
        indexName: 'ai-agency-os',
        contextualSearch: true,
      },
      colorMode: {
        defaultMode: 'light',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
    }),

  customFields: {
    stats: {
      agents: 68,
      skills: 292,
      routers: 19,
      views: 22,
      margin: '88%',
      pricing: ['$0 Free', '$49 Starter', '$199 Pro', '$999 Enterprise'],
      whitelabel: ['$199 Starter', '$499 Pro', '$999 Enterprise'],
      profitExample: '$14,701/month (98% margin) - 50 clients × $299 - $249 cost'
    }
  }
};

module.exports = config;
