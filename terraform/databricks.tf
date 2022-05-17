// The Terraform provider used to interact with Databricks.
// https://www.terraform.io/language/providers
//
// This default provider is used to create resources used to run our tests:
// - the service principal (databricks_service_principal). And,
// - the test compute cluster (databricks_cluster).
provider "databricks" {
  host = var.databricks_host

  // https://registry.terraform.io/providers/databrickslabs/databricks/latest/docs#authenticating-with-hostname-and-token
  token = var.databricks_token
}

// A service principal used to execute tests in the Databricks workspace.
// https://docs.databricks.com/administration-guide/users-groups/service-principals.html
// https://docs.microsoft.com/en-us/azure/databricks/administration-guide/users-groups/service-principals
//
// Running tests as a service principal is recommended, but not required. The service principal allows
// us to isolate tests, running them without individual user permissions and using minimal privileges.
resource "databricks_service_principal" "testrunner" {
  display_name = "Automation-only test runner SP"
}

// Permit the service principal created above to generate access tokens.
// https://registry.terraform.io/providers/databrickslabs/databricks/latest/docs/resources/permissions#token-usage
//
// This permission is a prerequisite for generating the token used by our GitHub Action to 
// authenticate to Databricks. (See 'databricks_obo_token' below.)
resource "databricks_permissions" "token_usage" {
  authorization = "tokens"
  access_control {
    service_principal_name = databricks_service_principal.testrunner.application_id
    permission_level       = "CAN_USE"
  }
}

// Create an authentication token for the service principal.
// https://registry.terraform.io/providers/databrickslabs/databricks/latest/docs/resources/obo_token
//
// The service principal authentication token is used by our GitHub Action to authenticate to the 
// Databricks workspace and run tests.
resource "databricks_obo_token" "testrunner_pat" {
  depends_on = [
    databricks_service_principal.testrunner
  ]
  comment  = "Test runner SP PAT"
  application_id = databricks_service_principal.testrunner.application_id
  lifetime_seconds = 3.156e+7 // 1 year, after which this must be refreshed.
}

// A second Databricks terraform provider that uses the service principal account created above.
//
// This service principal is used to run tests associated with GitHub pull requests.
provider "databricks" {
  alias = "sp-test"
  host = var.databricks_host
  token = databricks_obo_token.testrunner_pat.token_value
}

// Configure the GitHub authentication for the service principal.
// https://registry.terraform.io/providers/databrickslabs/databricks/latest/docs/resources/git_credential
//
// Authentication is required to clone a private repository.
resource "databricks_git_credential" "github" {
  provider = databricks.sp-test

  git_username = var.github_readonly_machine_user_name
  git_provider = "github"
  personal_access_token = var.github_readonly_machine_user_token
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
    permission_level = "CAN_RESTART"
  }
}

output "test_cluster_id" {
  value = databricks_cluster.shared_test_cluster.cluster_id
  description = "The cluster ID of the test cluster."
}
