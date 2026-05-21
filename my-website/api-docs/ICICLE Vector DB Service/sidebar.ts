import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebar: SidebarsConfig = {
  apisidebar: [
    {
      type: "doc",
      id: "ICICLE Vector DB Service/icicle-ai-vector-service",
    },
    {
      type: "category",
      label: "UNTAGGED",
      items: [
        {
          type: "doc",
          id: "ICICLE Vector DB Service/health-check-healthz-get",
          label: "Health Check",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/store-embedding-v-1-embeddings-post",
          label: "Store Embedding",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/update-user-embedding-v-1-embeddings-embedding-id-put",
          label: "Update User Embedding",
          className: "api-method put",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/delete-user-embedding-v-1-embeddings-embedding-id-delete",
          label: "Delete User Embedding",
          className: "api-method delete",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/retrieve-v-1-retrieve-post",
          label: "Retrieve",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/rerank-v-1-rerank-post",
          label: "Rerank",
          className: "api-method post",
        },
      ],
    },
  ],
};

export default sidebar.apisidebar;
