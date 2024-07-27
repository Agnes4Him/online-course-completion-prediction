variable "vpc_cidr" {
  description = "VPC cidr"
  default = ""
}

variable "vpc_tag" {
  description = "VPC tag"
  default = ""
}

variable "assume_role_policy" {
  description = "Assume role policy"
  default = ""
}

variable "assume_role_policy_autoscaler" {
  description = "Assume role policy for cluster autoscaler"
  default = ""
}

variable "node_group_instance_types" {
  type = list(string)
  description = "Instance types for node group"
  default = []
}