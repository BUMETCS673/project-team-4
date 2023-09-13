terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.00"
    }
  }
  backend "s3" {
    bucket = "terraform-state-09-12-2023-bu-cs673"
    key    = "flask-app"
    region = "us-east-1"
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "us-east-1"
}
