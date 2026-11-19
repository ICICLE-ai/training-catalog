import type { SidebarsConfig } from "@docusaurus/plugin-content-docs";

const sidebar: SidebarsConfig = {
  apisidebar: [
    {
      type: "doc",
      id: "ScienceAgent Interface/science-agent-api",
    },
    {
      type: "category",
      label: "Health",
      items: [
        {
          type: "doc",
          id: "ScienceAgent Interface/health-check-health-get-get",
          label: "Health Check",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/healthcheck-healthcheck-get-get",
          label: "Healthcheck",
          className: "api-method get",
        },
      ],
    },
    {
      type: "category",
      label: "Account",
      items: [
        {
          type: "doc",
          id: "ScienceAgent Interface/account-api-account-session-get-get",
          label: "Account",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/s-3-api-account-s-3-get-get",
          label: "S3",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/create-s-3-api-account-s-3-post-post",
          label: "Create S3",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/import-s-3-api-account-s-3-import-post-post",
          label: "Import S3",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/select-s-3-api-account-s-3-selection-put-put",
          label: "Select S3",
          className: "api-method put",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/update-s-3-api-account-s-3-profile-id-put-put",
          label: "Update S3",
          className: "api-method put",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/delete-s-3-api-account-s-3-profile-id-delete-delete",
          label: "Delete S3",
          className: "api-method delete",
        },
      ],
    },
    {
      type: "category",
      label: "Conversations",
      items: [
        {
          type: "doc",
          id: "ScienceAgent Interface/create-api-execution-agent-session-post-post",
          label: "Create",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/validate-api-execution-agent-session-validate-post-post",
          label: "Validate",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/sessions-api-execution-agent-sessions-get-get",
          label: "Sessions",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/delete-api-execution-agent-session-sid-delete-delete",
          label: "Delete",
          className: "api-method delete",
        },
      ],
    },
    {
      type: "category",
      label: "Attachments",
      items: [
        {
          type: "doc",
          id: "ScienceAgent Interface/upload-api-execution-upload-sid-post-post",
          label: "Upload",
          className: "api-method post",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/download-upload-api-execution-upload-sid-filename-get-get",
          label: "Download Upload",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/delete-upload-api-execution-upload-sid-filename-delete-delete",
          label: "Delete Upload",
          className: "api-method delete",
        },
      ],
    },
    {
      type: "category",
      label: "Tasks",
      items: [
        {
          type: "doc",
          id: "ScienceAgent Interface/benchmarks-api-tasks-get-get",
          label: "Benchmarks",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/detail-api-tasks-sid-get-get",
          label: "Detail",
          className: "api-method get",
        },
      ],
    },
    {
      type: "category",
      label: "Storage",
      items: [
        {
          type: "doc",
          id: "ScienceAgent Interface/storage-list-objects",
          label: "List Objects",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/storage-download-object",
          label: "Download Object",
          className: "api-method get",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/storage-delete-object",
          label: "Delete Object",
          className: "api-method delete",
        },
        {
          type: "doc",
          id: "ScienceAgent Interface/storage-delete-prefix",
          label: "Delete Prefix",
          className: "api-method delete",
        },
      ],
    },
  ],
};

export default sidebar.apisidebar;
