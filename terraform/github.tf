provider "github" {
  token = var.github_token
  owner = var.github_owner
}

resource "github_repository" "github_repository" {
  name = "notebook-best-practices"

  description = "An example showing how to apply software engineering best practices to Databricks notebooks."

  has_downloads = false
  has_issues = false
  has_projects = false
  has_wiki = false
}

resource "github_actions_secret" "github_actions_databricks_token" {
  repository = github_repository.github_repository.name
  secret_name = "DATABRICKS_TOKEN"
  plaintext_value = databricks_token.testrunner_pat.token_value
}
