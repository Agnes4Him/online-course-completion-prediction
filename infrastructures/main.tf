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

data "aws_iam_policy_document" "oidc_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringEquals"
      variable = "${replace(aws_iam_openid_connect_provider.eks.url, "https://", "")}:sub"
      values   = ["system:serviceaccount:default:aws-test"]
    }

    principals {
      identifiers = [aws_iam_openid_connect_provider.eks.arn]
      type        = "Federated"
    }
  }
}

data "aws_iam_policy_document" "eks_cluster_autoscaler_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringEquals"
      variable = "${replace(aws_iam_openid_connect_provider.eks.url, "https://", "")}:sub"
      values   = ["system:serviceaccount:kube-system:cluster-autoscaler"]
    }

    principals {
      identifiers = [aws_iam_openid_connect_provider.eks.arn]
      type        = "Federated"
    }
  }
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
  assume_role_policy = data.aws_iam_policy_document.oidc_assume_role_policy.json
  assume_role_policy_autoscaler = data.aws_iam_policy_document.eks_cluster_autoscaler_assume_role_policy.json
  node_group_instance_types = var.node_group_instance_types
}

module "rds" {
  source = "./modules/rds"
  subnet_ids = [module.eks.aws_subnet.db_subnetA, module.eks.aws_subnet.db_subnetB] 
  vpc_id = module.eks.aws_vpc.model_vpc.id
  db_username = var.db_username
  db_password = var.db_password
}

data "aws_db_instance" "postgres_db" {
  db_instance_identifier = "model_db"
}

output "rds_host" {
  value = data.aws_db_instance.postgres_db.host
}

output "rds_username" {
  value = data.aws_db_instance.postgres_db.master_username
}

output "rds_password" {
  value = data.aws_db_instance.postgres_db.password
}

output "ecr_repo" {
  value = "${var.ecr_repo_name}_${var.project_id}"
}