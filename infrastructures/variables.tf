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

variable "db_username" {
  description = "DB username"
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

variable "node_group_instance_types" {
  type = list(string)
  description = "Instance types for node group"
  default = ["t3.small"]
}