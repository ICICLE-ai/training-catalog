import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebar: SidebarsConfig = {
  apisidebar: [
    {
      type: "doc",
      id: "Project-1 APIs/project-1-apis",
    },
    {
      type: "category",
      label: "Project-1 APIs",
      items: [
        {
          type: "doc",
          id: "Project-1 APIs/list-all-models",
          label: "List all Models",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Project-1 APIs/single-model-info",
          label: "Single model info",
          className: "api-method get",
        },
      ],
    },
  ],
};

export default sidebar.apisidebar;
