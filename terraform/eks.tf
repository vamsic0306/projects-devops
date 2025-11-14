# eks placeholder
###############################################################
# EKS Cluster + Managed Node Groups (Best Practice)
###############################################################

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.30"

  ##############################################################
  # Network Integration (Private Subnets for Nodes)
  ##############################################################
  vpc_id  = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets  # Worker nodes stay private

  ##############################################################
  # Enable EKS Addons (Recommended)
  ##############################################################
  cluster_addons = {
    vpc-cni = {
      most_recent = true
    }
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
  }

  ##############################################################
  # Managed Node Groups (Recommended by AWS)
  ##############################################################
  eks_managed_node_groups = {
    ecommerce_nodes = {
      min_size     = 2
      max_size     = 5
      desired_size = 3

      instance_types = [var.instance_type] # t3.large

      # Nodes live inside private subnets (best practice)
      subnet_ids = module.vpc.private_subnets

      # Allow SSH via SSM
      remote_access = {
        ec2_ssh_key               = null
        source_security_group_ids = null
      }
    }
  }

  ##############################################################
  # Tags (mandatory for AWS load balancers)
  ##############################################################
  tags = {
    "Project"        = "Ecommerce-DevOps"
    "Environment"    = "Production"
  }
}
