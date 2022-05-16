terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "~> 4.0"
    }
    databricks = {
      source  = "databrickslabs/databricks"
      version = "~> 0.5"
    }
  }
}
