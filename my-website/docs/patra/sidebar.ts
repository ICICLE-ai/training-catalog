import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebar: SidebarsConfig = {
  apisidebar: [
    {
      type: "doc",
      id: "patra/patra-apis",
    },
    {
      type: "category",
      label: "Patra APIs",
      items: [
        {
          type: "doc",
          id: "patra/list-all-models",
          label: "List all Models",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "patra/single-model-info",
          label: "Single model info",
          className: "api-method get",
        },
      ],
    },
  ],
};

export default sidebar.apisidebar;
