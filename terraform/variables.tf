###############################################
# Variables for Reusability & Flexibility
###############################################

# AWS region
variable "aws_region" {
  description = "AWS region where resources will be created"
  type        = string
  default     = "ap-south-1"
}

# VPC CIDR block
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

# Public subnets (Mumbai has 3 AZs)
variable "public_subnets" {
  description = "Public subnets for Load Balancers, NAT"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

# Private subnets (worker nodes)
variable "private_subnets" {
  description = "Private subnets used by EKS worker nodes"
  type        = list(string)
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

# EKS cluster name
variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "ecommerce-eks"
}

# EC2 node instance type
variable "instance_type" {
  description = "Instance type for EKS worker nodes"
  type        = string
  default     = "t3.large"
}
