import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebar: SidebarsConfig = {
  apisidebar: [
    {
      type: "doc",
      id: "FAF APIs/faf-apis",
    },
    {
      type: "category",
      label: "commodity_total",
      items: [
        {
          type: "doc",
          id: "FAF APIs/commodity-total-list",
          label: "commodity_total_list",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "FAF APIs/commodity-total-create",
          label: "commodity_total_create",
          className: "api-method post",
        },
      ],
    },
    {
      type: "category",
      label: "data_option",
      items: [
        {
          type: "doc",
          id: "FAF APIs/data-option-retrieve",
          label: "data_option_retrieve",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "FAF APIs/data-option-create",
          label: "data_option_create",
          className: "api-method post",
        },
      ],
    },
    {
      type: "category",
      label: "exports_imports_details",
      items: [
        {
          type: "doc",
          id: "FAF APIs/exports-imports-details-list",
          label: "exports_imports_details_list",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "FAF APIs/exports-imports-details-create",
          label: "exports_imports_details_create",
          className: "api-method post",
        },
      ],
    },
    {
      type: "category",
      label: "exports_imports_mode_details",
      items: [
        {
          type: "doc",
          id: "FAF APIs/exports-imports-mode-details-list",
          label: "exports_imports_mode_details_list",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "FAF APIs/exports-imports-mode-details-create",
          label: "exports_imports_mode_details_create",
          className: "api-method post",
        },
      ],
    },
    {
      type: "category",
      label: "get_bar_chart_details",
      items: [
        {
          type: "doc",
          id: "FAF APIs/get-bar-chart-details-create",
          label: "get_bar_chart_details_create",
          className: "api-method post",
        },
      ],
    },
    {
      type: "category",
      label: "get_domestic_flow_details",
      items: [
        {
          type: "doc",
          id: "FAF APIs/get-domestic-flow-details-retrieve",
          label: "get_domestic_flow_details_retrieve",
          className: "api-method get",
        },
      ],
    },
    {
      type: "category",
      label: "get_foreign_export_details",
      items: [
        {
          type: "doc",
          id: "FAF APIs/get-foreign-export-details-retrieve",
          label: "get_foreign_export_details_retrieve",
          className: "api-method get",
        },
      ],
    },
    {
      type: "category",
      label: "get_foreign_import_details",
      items: [
        {
          type: "doc",
          id: "FAF APIs/get-foreign-import-details-retrieve",
          label: "get_foreign_import_details_retrieve",
          className: "api-method get",
        },
      ],
    },
    {
      type: "category",
      label: "get_table_data",
      items: [
        {
          type: "doc",
          id: "FAF APIs/get-table-data-create",
          label: "get_table_data_create",
          className: "api-method post",
        },
      ],
    },
    {
      type: "category",
      label: "import_export_sum",
      items: [
        {
          type: "doc",
          id: "FAF APIs/import-export-sum-create",
          label: "import_export_sum_create",
          className: "api-method post",
        },
      ],
    },
    {
      type: "category",
      label: "point_to_point",
      items: [
        {
          type: "doc",
          id: "FAF APIs/point-to-point-list",
          label: "point_to_point_list",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "FAF APIs/point-to-point-create",
          label: "point_to_point_create",
          className: "api-method post",
        },
      ],
    },
  ],
};

export default sidebar.apisidebar;
