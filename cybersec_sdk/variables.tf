variable "aws_region" {
  description = "The AWS region to deploy into."
  type        = string
  default     = "us-east-1"
}

variable "key_pair_name" {
  description = "The name of the AWS key pair to use for SSH access."
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC where the instance will be deployed."
  type        = string
}

variable "my_ip" {
  description = "Your IP address to allow SSH access (in CIDR notation)."
  type        = string
}

variable "neo4j_password" {
  description = "Password for the Neo4j database."
  type        = string
}

variable "ec2_instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t2.micro"
}

variable "neo4j_uri" {
  description = "URI for the Neo4j database."
  type        = string
}

variable "neo4j_user" {
  description = "Username for the Neo4j database."
  type        = string
  default     = "neo4j"
}

