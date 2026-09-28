import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebar: SidebarsConfig = {
  apisidebar: [
    {
      type: "doc",
      id: "ICICLE Vector DB Service/icicle-ai-vector-service",
    },
    {
      type: "category",
      label: "health",
      items: [
        {
          type: "doc",
          id: "ICICLE Vector DB Service/health-check-healthz-get",
          label: "Health Check",
          className: "api-method get",
        },
      ],
    },
    {
      type: "category",
      label: "embeddings",
      items: [
        {
          type: "doc",
          id: "ICICLE Vector DB Service/store-embedding-v-1-embeddings-post",
          label: "Store an embedding",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/bulk-delete-v-1-embeddings-bulk-delete-post",
          label: "Delete many embeddings in one collection",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/read-embedding-v-1-embeddings-embedding-id-get",
          label: "Get one embedding",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/update-user-embedding-v-1-embeddings-embedding-id-put",
          label: "Update an embedding",
          className: "api-method put",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/delete-user-embedding-v-1-embeddings-embedding-id-delete",
          label: "Delete an embedding",
          className: "api-method delete",
        },
      ],
    },
    {
      type: "category",
      label: "collections",
      items: [
        {
          type: "doc",
          id: "ICICLE Vector DB Service/list-collections-v-1-collections-get",
          label: "List your collections",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/purge-all-v-1-collections-delete",
          label: "Delete ALL your embeddings across every collection",
          className: "api-method delete",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/read-collection-v-1-collections-collection-get",
          label: "Get one collection's stats",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/delete-collection-v-1-collections-collection-delete",
          label: "Delete your embeddings in one collection",
          className: "api-method delete",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/list-embeddings-v-1-collections-collection-embeddings-get",
          label: "List your embeddings in a collection",
          className: "api-method get",
        },
      ],
    },
    {
      type: "category",
      label: "search",
      items: [
        {
          type: "doc",
          id: "ICICLE Vector DB Service/retrieve-v-1-retrieve-post",
          label: "Vector similarity search",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/rerank-methods-v-1-rerank-methods-get",
          label: "List available rerank methods",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ICICLE Vector DB Service/rerank-v-1-rerank-post",
          label: "Rerank search results",
          className: "api-method post",
        },
      ],
    },
  ],
};

export default sidebar.apisidebar;
