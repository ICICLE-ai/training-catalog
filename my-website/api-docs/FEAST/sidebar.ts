import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebar: SidebarsConfig = {
  apisidebar: [
    {
      type: "doc",
      id: "FEAST/food-access-model-api",
    },
    {
      type: "category",
      label: "ABM",
      items: [
        {
          type: "doc",
          id: "FEAST/get-simulation-instances-api-simulation-instances-get",
          label: "Get Simulation Instances",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "FEAST/create-simulation-instance-api-simulation-instances-post",
          label: "Create Simulation Instance",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "FEAST/get-simulation-instance-api-simulation-instances-instance-id-get",
          label: "Get Simulation Instance",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "FEAST/delete-simulation-instance-api-simulation-instances-instance-id-delete",
          label: "Delete Simulation Instance",
          className: "api-method delete",
        },
        {
          type: "doc",
          id: "FEAST/advance-simulation-instance-api-simulation-instances-instance-id-advance-post",
          label: "Advance Simulation Instance",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "FEAST/reset-simulation-instance-api-simulation-instances-instance-id-reset-post",
          label: "Reset Simulation Instance",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "FEAST/get-all-households-api-households-get",
          label: "Get All Households",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "FEAST/get-stores-api-stores-get",
          label: "Get Stores",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "FEAST/add-store-api-stores-post",
          label: "Add Store",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "FEAST/remove-store-api-stores-delete",
          label: "Remove Store",
          className: "api-method delete",
        },
        {
          type: "doc",
          id: "FEAST/get-step-number-api-get-step-number-get",
          label: "Get Step Number",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "FEAST/get-num-households-api-get-num-households-get",
          label: "Get Num Households",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "FEAST/get-num-stores-api-get-num-stores-get",
          label: "Get Num Stores",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "FEAST/get-household-stats-api-get-household-stats-get",
          label: "Get Household Stats",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "FEAST/health-check-api-health-get",
          label: "Health Check",
          className: "api-method get",
        },
      ],
    },
  ],
};

export default sidebar.apisidebar;
