# outputs placeholder
###############################################################
# Terraform Outputs — Used After "terraform apply"
###############################################################

output "eks_cluster_name" {
  description = "EKS Cluster Name"
  value       = module.eks.cluster_name
}

output "eks_cluster_endpoint" {
  description = "EKS API Server Endpoint"
  value       = module.eks.cluster_endpoint
}

output "eks_oidc_provider" {
  description = "OIDC Provider for IAM Roles"
  value       = module.eks.oidc_provider
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "private_subnets" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnets
}

output "public_subnets" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnets
}

##############################
# Output DB Endpoints
##############################

output "users_db_endpoint" {
  value = aws_db_instance.users_db.endpoint
}

output "orders_db_endpoint" {
  value = aws_db_instance.orders_db.endpoint
}

output "payments_db_endpoint" {
  value = aws_db_instance.payments_db.endpoint
}
