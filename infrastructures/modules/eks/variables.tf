variable "vpc_cidr" {
  description = "VPC cidr"
  default = ""
}

variable "vpc_tag" {
  description = "VPC tag"
  default = ""
}

variable "node_group_instance_types" {
  type = list(string)
  description = "Instance types for node group"
  default = []
}