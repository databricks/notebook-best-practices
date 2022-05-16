provider "databricks" {
  host = var.databricks_host
  token = var.databricks_token
}

resource "databricks_service_principal" "testrunner" {
  display_name = "Automation-only test runner SP"
}

resource "databricks_permissions" "token_usage" {
  authorization = "tokens"
  access_control {
    service_principal_name = databricks_service_principal.testrunner.application_id
    permission_level       = "CAN_USE"
  }
}

resource "databricks_obo_token" "testrunner_pat" {
  depends_on = [
    databricks_service_principal.testrunner
  ]
  comment  = "Test runner SP PAT"
  application_id = databricks_service_principal.testrunner.application_id
  lifetime_seconds = 3.156e+7 # 1 year
}

provider "databricks" {
  alias = "sp"
  host = var.databricks_host
  token = databricks_obo_token.testrunner_pat.token_value
}

resource "databricks_git_credential" "github" {
  provider = databricks.sp

  git_username = var.github_username
  git_provider = "github"
  personal_access_token = var.github_token
}
