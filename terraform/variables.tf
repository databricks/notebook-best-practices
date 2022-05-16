variable "databricks_host" {
  description = "The host of the Databricks Workspace. Example: https://demo.cloud.databricks.com/"
  type        = string
}

variable "databricks_token" {
  description = "The PAT used to authenticate to the Databricks Workspace specified by databricks_host."
  type        = string
  sensitive   = true
}

variable "github_owner" {
  description = "The owner of the GitHub repostiory. Example: Databricks"
  type        = string
}

# TODO: Add a warning about SP GitHub permissions.
variable "github_username" {
  description = "Your GitHub username."
  type        = string
}

variable "github_repository_name" {
  description = "The name of the GitHub repostiory. Example: notebook-best-practices"
  type        = string
}

variable "github_token" {
  description = "A GitHub authentication token."
  type        = string
  sensitive   = true
}
