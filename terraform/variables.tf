variable "databricks_host" {
  description = "The host of the Databricks Workspace. Example: https://db-sme-demo-docs.cloud.databricks.com/"
  type        = string
}

variable "databricks_token" {
  description = "The PAT used to authenticate to the Databricks Workspace specified by databricks_host."
  type        = string
  sensitive   = true
}

variable "github_owner" {
  description = "The organization owner of the GitHub repostiory. Example: Databricks"
  type        = string
}

variable "github_repository_name" {
  description = "The name of the GitHub repostiory. Example: notebook-best-practices"
  type        = string
}

variable "github_repo_admin_token" {
  description = "A GitHub authentication token with admin permission for github_repository_name. This is used to configure branch protection and required pre-merge tests."
  type        = string
  sensitive   = true
}

variable "github_readonly_machine_user_name" {
  description = "A GitHub username with at least read-only access to github_repository_name. This is used by the databricks_host workspace when cloning a private repository."
  type        = string
}

variable "github_readonly_machine_user_token" {
  description = "A GitHub authentication token with at least read-only access to github_repository_name. This is used by the databricks_host workspace when cloning a private repository."
  type        = string
  sensitive   = true
}
