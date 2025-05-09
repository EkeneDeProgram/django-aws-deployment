output "ec2_public_ip" {
  value = aws_instance.django_server.public_ip
}

data "aws_db_instance" "existing_postgres" {
  db_instance_identifier = "django-db"  # Your DB instance identifier
}

output "rds_endpoint" {
  value = data.aws_db_instance.existing_postgres.endpoint  # This will fetch the endpoint of your RDS
}

