variable "AWS_ACCESS_KEY_ID" {
  description = "AWS Access Key ID"
  type        = string
  sensitive   = true
}

variable "AWS_SECRET_ACCESS_KEY" {
  description = "AWS Secret Access Key"
  type        = string
  sensitive   = true
}

variable "AWS_DEFAULT_REGION" {
  description = "The AWS region"
  type        = string
}

variable "KEY_NAME" {
  description = "The SSH key name for EC2"
  type        = string
}

variable "AWS_DB_PASSWORD" {
  description = "The database password"
  type        = string
  sensitive   = true
}

