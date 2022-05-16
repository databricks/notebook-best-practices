provider "github" {
  token = var.github_token
  owner = var.github_owner
}

resource "github_repository" "github_repository" {
  name = "notebook-best-practices"

  description = "An example showing how to apply software engineering best practices to Databricks notebooks."

  has_downloads = false
  has_issues    = false
  has_projects  = false
  has_wiki      = false

  # https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges#squash-and-merge-your-pull-request-commits
  allow_auto_merge   = false
  allow_merge_commit = false
  allow_rebase_merge = false
  allow_squash_merge = true
}

# https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches#require-status-checks-before-merging
resource "github_branch_protection" "main" {
  depends_on = [github_repository.github_repository]

  allows_deletions                = false
  allows_force_pushes             = false
  enforce_admins                  = true
  pattern                         = "main"
  push_restrictions               = []
  require_conversation_resolution = false
  require_signed_commits          = false
  required_linear_history         = true
  repository_id                   = github_repository.github_repository.name

  required_status_checks {
    contexts = ["unit-test-notebook", "covid-eda-notebook"]
    strict   = true
  }
}

resource "github_actions_secret" "github_actions_databricks_token" {
  repository      = github_repository.github_repository.name
  secret_name     = "DATABRICKS_TOKEN"
  plaintext_value = databricks_obo_token.testrunner_pat.token_value
}
