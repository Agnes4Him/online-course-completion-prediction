resource "random_password" "db_password" {
  length           = 16 
  min_lower        = 1
  min_upper        = 1
  min_numeric      = 1
  min_special      = 1
  override_special = "!#$%&*()-_=+[]{}<>:?" 
}

resource "aws_db_instance" "model_db" {
  identifier             = "model-db"
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "14.1"
  username               = var.db_username
  password               = random_password.db_password.result
  db_subnet_group_name   = aws_db_subnet_group.rds_subnets.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  publicly_accessible    = true
  skip_final_snapshot    = true
  depends_on = [random_password.db_password]
}

output "rds_host" {
  value = aws_db_instance.model_db.address
}

output "rds_username" {
  value = aws_db_instance.model_db.username
}

output "rds_password" {
  value = aws_db_instance.model_db.password
}