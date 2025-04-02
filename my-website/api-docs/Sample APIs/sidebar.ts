import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebar: SidebarsConfig = {
  apisidebar: [
    {
      type: "doc",
      id: "Sample APIs/api-documentation",
    },
    {
      type: "category",
      label: "Example",
      items: [
        {
          type: "doc",
          id: "Sample APIs/create-an-example-resource",
          label: "Create an example resource",
          className: "api-method post",
        },
      ],
    },
  ],
};

export default sidebar.apisidebar;
