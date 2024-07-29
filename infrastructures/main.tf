terraform {
  required_version = ">= 1.0"
  #backend "s3" {
    #bucket  = "tf-state-mlops-zoomcamp-capstone-project"
    #key     = "mlops-zoomcamp.tfstate"
    #region  = "us-east-1"
    #encrypt = true
  #}
}

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current_identity" {}

data "aws_availability_zones" "available" {}

locals {
  account_id = data.aws_caller_identity.current_identity.account_id
}

# image registry
module "ecr_repo" {
   source = "./modules/ecr"
   ecr_repo_name = "${var.ecr_repo_name}_${var.project_id}"
}

module "eks" {
  source = "./modules/eks"
  vpc_cidr = var.vpc_cidr
  vpc_tag = var.vpc_tag
  node_group_instance_types = var.node_group_instance_types
}

module "rds" {
  source = "./modules/rds"
  subnet_ids = [module.eks.db_subnetA, module.eks.db_subnetB]
  vpc_id = module.eks.vpc_id
  db_username = var.db_username
}

output "rds_host" {
  value = module.rds.rds_host
}

output "rds_username" {
  value = module.rds.rds_username
}

output "rds_password" {
  value     = module.rds.rds_password
  sensitive = true
}

output "ecr_repo" {
  value = "${var.ecr_repo_name}_${var.project_id}"
}