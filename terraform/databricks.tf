provider "databricks" {
  profile = "demo"
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

resource "databricks_token" "testrunner_pat" {
  comment  = "Test runner SP PAT"
  lifetime_seconds = 0
}
