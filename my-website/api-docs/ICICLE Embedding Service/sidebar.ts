import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebar: SidebarsConfig = {
  apisidebar: [
    {
      type: "doc",
      id: "ICICLE Embedding Service/icicle-ai-embed-service",
    },
    {
      type: "category",
      label: "UNTAGGED",
      items: [
        {
          type: "doc",
          id: "ICICLE Embedding Service/health-check-healthz-get",
          label: "Health Check",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ICICLE Embedding Service/model-info-v-1-model-get",
          label: "Model Info",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ICICLE Embedding Service/embed-v-1-embed-post",
          label: "Embed",
          className: "api-method post",
        },
      ],
    },
  ],
};

export default sidebar.apisidebar;
