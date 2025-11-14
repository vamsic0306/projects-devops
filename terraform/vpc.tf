# vpc placeholder
##############################################################
# VPC with Public + Private Subnets + NAT (BEST PRACTICE)
##############################################################

module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "ecommerce-vpc"

  # CIDR for whole VPC
  cidr = var.vpc_cidr

  # AZs in ap-south-1
  azs = ["ap-south-1a", "ap-south-1b"]

  ############################################################
  # PUBLIC Subnets -> Used for: Load Balancers, NAT Gateway
  ############################################################
  public_subnets = var.public_subnets

  ############################################################
  # PRIVATE Subnets -> Used for: EKS Worker Nodes (secure)
  ############################################################
  private_subnets = var.private_subnets

  # Enable NAT Gateway (so private nodes access internet)
  enable_nat_gateway = true
  single_nat_gateway = true

  # Public subnets will have IGW routing
  map_public_ip_on_launch = false

  # Tags for k8s AWS Load Balancer Controller
  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = "1"
  }
}
