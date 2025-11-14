###############################################################
# RDS PostgreSQL Instances for Each Microservice
# users-db, orders-db, payments-db
###############################################################

#-------------------------#
# DB Subnet Group (Private)
#-------------------------#
resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "ecommerce-db-subnet-group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name = "ecommerce-db-subnet-group"
  }
}

#-------------------------#
# Security Group for RDS
#-------------------------#
resource "aws_security_group" "rds_sg" {
  name        = "rds-sg"
  description = "Allow EKS nodes to access RDS"
  vpc_id      = module.vpc.vpc_id
}

# Allow only private subnets + EKS nodes access to DB
resource "aws_security_group_rule" "allow_eks_to_db" {
  type              = "ingress"
  from_port         = 5432
  to_port           = 5432
  protocol          = "tcp"
  security_group_id = aws_security_group.rds_sg.id
  cidr_blocks       = module.vpc.private_subnets_cidr_blocks
}

# Egress (DB will need outbound to internet for patches)
resource "aws_security_group_rule" "allow_db_egress" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  security_group_id = aws_security_group.rds_sg.id
  cidr_blocks       = ["0.0.0.0/0"]
}

##############################
# DB 1 → users-db
##############################
resource "aws_db_instance" "users_db" {
  identifier         = "users-db"
  engine             = "postgres"
  engine_version     = "14.10"
  instance_class     = "db.t3.micro"
  allocated_storage  = 20

  db_name            = "usersdb"
  username           = "users_admin"
  password           = "UsersDB@12345" # Move to SSM later

  publicly_accessible = false
  skip_final_snapshot = true

  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.name
}

##############################
# DB 2 → orders-db
##############################
resource "aws_db_instance" "orders_db" {
  identifier         = "orders-db"
  engine             = "postgres"
  engine_version     = "14.10"
  instance_class     = "db.t3.micro"
  allocated_storage  = 20

  db_name            = "ordersdb"
  username           = "orders_admin"
  password           = "OrdersDB@12345"

  publicly_accessible = false
  skip_final_snapshot = true

  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.name
}

##############################
# DB 3 → payments-db
##############################
resource "aws_db_instance" "payments_db" {
  identifier         = "payments-db"
  engine             = "postgres"
  engine_version     = "14.10"
  instance_class     = "db.t3.micro"
  allocated_storage  = 20

  db_name            = "paymentsdb"
  username           = "payments_admin"
  password           = "PaymentsDB@12345"

  publicly_accessible = false
  skip_final_snapshot = true

  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.name
}
