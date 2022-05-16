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

// TODO: Document the rationale for this separate provider.
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

data "databricks_node_type" "smallest" {
  local_disk = true
}

data "databricks_spark_version" "latest_lts" {
  long_term_support = true
}

resource "databricks_cluster" "shared_test_cluster" {
  cluster_name            = "Shared test cluster"
  spark_version           = data.databricks_spark_version.latest_lts.id
  node_type_id            = data.databricks_node_type.smallest.id
  autotermination_minutes = 120
  autoscale {
    min_workers = 1
    max_workers = 5
  }
}

resource "databricks_permissions" "cluster_usage" {
  cluster_id = databricks_cluster.shared_test_cluster.cluster_id

  access_control {
    user_name       = databricks_service_principal.testrunner.application_id
    permission_level = "CAN_ATTACH_TO"
  }
}

output "test_cluster_id" {
  value = databricks_cluster.shared_test_cluster.cluster_id
  description = "The cluster ID of the test cluster."
}
