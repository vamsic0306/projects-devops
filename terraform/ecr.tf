# ecr placeholder
###############################################################
# ECR Repositories for Docker Images of All Microservices
###############################################################

resource "aws_ecr_repository" "frontend" {
  name = "ecommerce-frontend"
  image_tag_mutability = "MUTABLE"

  tags = {
    Project = "Ecommerce-DevOps"
  }
}

resource "aws_ecr_repository" "users" {
  name = "ecommerce-users"
  image_tag_mutability = "MUTABLE"

  tags = {
    Project = "Ecommerce-DevOps"
  }
}

resource "aws_ecr_repository" "orders" {
  name = "ecommerce-orders"
  image_tag_mutability = "MUTABLE"

  tags = {
    Project = "Ecommerce-DevOps"
  }
}

resource "aws_ecr_repository" "payments" {
  name = "ecommerce-payments"
  image_tag_mutability = "MUTABLE"

  tags = {
    Project = "Ecommerce-DevOps"
  }
}
