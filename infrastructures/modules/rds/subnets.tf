resource "aws_db_subnet_group" "rds_subnets" {
  name       = "db_subnet_group"
  subnet_ids = var.subnet_ids

  tags = {
    Name = "DBSubnet"
  }
}