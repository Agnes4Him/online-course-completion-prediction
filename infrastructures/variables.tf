variable "aws_region" {
  description = "AWS region to create resources"
  default     = "us-east-1"
}

variable "project_id" {
  description = "project_id"
  default = "mlops-zoomcamp-capstone"
}

variable "ecr_repo_name" {
  description = ""
  default = ""
}

variable "model_bucket" {
  description = "s3_bucket"
  default = ""
}

variable "db_username" {
  description = "DB username"
  default = ""
}

variable "db_password" {
  description = "DB password"
  default = ""
}

variable "vpc_cidr" {
  description = "VPC cidr block"
  default = "10.0.0.0/16"
}

variable "vpc_tag" {
  description = "VPC tag"
  default = "ModelVPC"
}

