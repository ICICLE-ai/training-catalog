import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebar: SidebarsConfig = {
  apisidebar: [
    {
      type: "doc",
      id: "Patra Knowledge Base/patra-ai-cards-api",
    },
    {
      type: "category",
      label: "model_cards",
      items: [
        {
          type: "doc",
          id: "Patra Knowledge Base/list-model-cards-modelcards-get",
          label: "List Model Cards",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/get-model-card-modelcard-uuid-get",
          label: "Get Model Card",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/update-model-card-modelcard-uuid-put",
          label: "Update Model Card",
          className: "api-method put",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/get-model-download-url-modelcard-uuid-download-url-get",
          label: "Get Model Download Url",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/get-model-deployments-modelcard-uuid-deployments-get",
          label: "Get Model Deployments",
          className: "api-method get",
        },
      ],
    },
    {
      type: "category",
      label: "datasheets",
      items: [
        {
          type: "doc",
          id: "Patra Knowledge Base/list-datasheets-datasheets-get",
          label: "List Datasheets",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/get-datasheet-datasheet-uuid-get",
          label: "Get Datasheet",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/update-datasheet-datasheet-uuid-put",
          label: "Update Datasheet",
          className: "api-method put",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/delete-datasheet-datasheet-uuid-delete",
          label: "Delete Datasheet",
          className: "api-method delete",
        },
      ],
    },
    {
      type: "category",
      label: "assets",
      items: [
        {
          type: "doc",
          id: "Patra Knowledge Base/create-model-card-asset-v-1-assets-model-cards-post",
          label: "Create Model Card Asset",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/create-datasheet-asset-v-1-assets-datasheets-post",
          label: "Create Datasheet Asset",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/list-editable-records-v-1-assets-records-get",
          label: "List Editable Records",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/update-model-card-asset-v-1-assets-model-cards-asset-id-patch",
          label: "Update Model Card Asset",
          className: "api-method patch",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/update-datasheet-asset-v-1-assets-datasheets-asset-id-patch",
          label: "Update Datasheet Asset",
          className: "api-method patch",
        },
      ],
    },
    {
      type: "category",
      label: "agent-tools",
      items: [
        {
          type: "doc",
          id: "Patra Knowledge Base/get-schema-pool-agent-tools-schema-pool-get",
          label: "Get Schema Pool",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/paper-schema-search-agent-tools-paper-schema-search-post",
          label: "Paper Schema Search",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/paper-schema-search-upload-agent-tools-paper-schema-search-upload-post",
          label: "Paper Schema Search Upload",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/missing-column-analysis-agent-tools-missing-column-analysis-post",
          label: "Missing Column Analysis",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/generate-synthesized-dataset-route-agent-tools-generate-synthesized-dataset-post",
          label: "Generate Synthesized Dataset Route",
          className: "api-method post",
        },
      ],
    },
    {
      type: "category",
      label: "users",
      items: [
        {
          type: "doc",
          id: "Patra Knowledge Base/register-user-users-post",
          label: "Register User",
          className: "api-method post",
        },
      ],
    },
    {
      type: "category",
      label: "ask-patra",
      items: [
        {
          type: "doc",
          id: "Patra Knowledge Base/ask-patra-bootstrap-api-ask-patra-bootstrap-get",
          label: "Ask Patra Bootstrap",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/ask-patra-chat-api-ask-patra-chat-post",
          label: "Ask Patra Chat",
          className: "api-method post",
        },
      ],
    },
    {
      type: "category",
      label: "experiments",
      items: [
        {
          type: "doc",
          id: "Patra Knowledge Base/list-experiment-users-experiments-domain-users-get",
          label: "List Experiment Users",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/get-user-experiment-summary-experiments-domain-users-user-id-summary-get",
          label: "Get User Experiment Summary",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/list-user-experiments-experiments-domain-users-user-id-list-get",
          label: "List User Experiments",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/get-experiment-detail-experiments-domain-experiment-id-get",
          label: "Get Experiment Detail",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/get-experiment-images-experiments-domain-experiment-id-images-get",
          label: "Get Experiment Images",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/get-experiment-power-experiments-domain-experiment-id-power-get",
          label: "Get Experiment Power",
          className: "api-method get",
        },
      ],
    },
    {
      type: "category",
      label: "hf-import",
      items: [
        {
          type: "doc",
          id: "Patra Knowledge Base/preview-hf-import-v-1-hf-import-preview-post",
          label: "Preview Hf Import",
          className: "api-method post",
        },
      ],
    },
    {
      type: "category",
      label: "UNTAGGED",
      items: [
        {
          type: "doc",
          id: "Patra Knowledge Base/root-get",
          label: "Root",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/healthz-healthz-get",
          label: "Healthz",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "Patra Knowledge Base/readyz-readyz-get",
          label: "Readyz",
          className: "api-method get",
        },
      ],
    },
  ],
};

export default sidebar.apisidebar;
