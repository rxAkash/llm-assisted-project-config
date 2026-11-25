terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
  # backend "s3" {}  # configure remote state per environment
}

provider "aws" {
  region = var.region
}

variable "region" {
  type    = string
  default = "eu-west-1"
}

module "postgres" {
  source      = "../../modules/postgres"
  name        = "dp-dev"
  db_password = var.db_password
}

variable "db_password" {
  type      = string
  sensitive = true
}
