variable "github_owner" {
    description = "The owner of the GitHub repostiory."
    type = string
}

variable "github_repository_name" {
    description = "The name of the GitHub repostiory."
    type = string
}

variable "github_token" {
    description = "A GitHub authentication token."
    type = string
    sensitive = true
}
