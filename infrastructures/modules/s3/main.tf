resource "aws_s3_bucket" "model_bucket" {
  bucket = var.bucket_name
  force_destroy = true
  tags    = {
	Name          = "ModelBucket"
  }
}

resource "aws_s3_bucket_acl" "example" {
  bucket = aws_s3_bucket.model_bucket.id
  acl    = "private"
}

output "name" {
  value = aws_s3_bucket.s3_bucket.bucket
}