terraform {
  required_version = ">= 1.0"
  backend "s3" {
    bucket  = "tf-state-mlops-zoomcamp-capstone-project"
    key     = "mlops-zoomcamp.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
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

module "s3_bucket" {
  source = "./modules/s3"
  bucket_name = "${var.model_bucket}-${var.project_id}"
}

module "eks" {
  source = "./modules/eks"
  vpc_cidr = var.vpc_cidr
  vpc_tag = var.vpc_tag
}

module "rds" {
  source = "./modules/rds"
  subnet_ids = [module.eks.aws_subnet.db_subnetA, module.eks.aws_subnet.db_subnetB] 
  vpc_id = module.eks.aws_vpc.model_vpc.id
  db_username = var.db_username
  db_password = var.db_password
}





output "model_bucket" {
  value = module.s3_bucket.name
}

output "ecr_repo" {
  value = "${var.ecr_repo_name}_${var.project_id}"
}