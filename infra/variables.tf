# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-west-1"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "docker-chroma-db-lab"
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket for processed pipeline data"
  type        = string
}
