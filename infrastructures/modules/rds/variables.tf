variable "subnet_ids" {
  description = "List of subnets for Postgres DB"
  default     = []
}

variable "vpc_id" {
  description = "The id of VPC for Postgres DB"
  default     = ""
}

variable "db_username" {
  description = "DB username"
  default = ""
}

variable "db_password" {
  description = "DB password"
  default = ""
}
