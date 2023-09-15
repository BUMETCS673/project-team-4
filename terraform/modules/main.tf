##############
## TF State ##
##############

terraform {
  backend "s3" {
    bucket = "terraform-state-09-12-2023-bu-cs673"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}

###################
## ACM Resources ##
###################

resource "aws_acm_certificate" "domain_cert" {
  domain_name       = "bumtelevision.com"
  validation_method = "DNS"

  tags = {
    Environment = "flask-app-cert"
  }

  lifecycle {
    create_before_destroy = true
  }
}

###################
## ALB Resources ##
###################


##########################
## CloudWatch Resources ##
##########################



###################
## ECS Resources ##
###################

resource "aws_ecs_cluster" "flask_cluster" {
  name = "flask-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

###################
## IAM Resources ##
###################


###################
## KMS Resources ##
###################


######################
## Lambda Resources ##
######################


########################
## Route-53 Resources ##
########################


###############################
## Secrets Manager Resources ##
###############################



###################
## VPC Resources ##
###################

resource "aws_vpc" "flask_app_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "flask-app-vpc"
  }
}

resource "aws_subnet" "flask_app_subnet_1a" {
  availability_zone = "us-east-1a"
  cidr_block        = "10.0.1.0/24"
  vpc_id            = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-subnet-1a"
  }
}

resource "aws_subnet" "flask_app_subnet_1b" {
  availability_zone = "us-east-1b"
  cidr_block        = "10.0.2.0/24"
  vpc_id            = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-subnet-1b"
  }
}

resource "aws_subnet" "flask_app_subnet_1c" {
  availability_zone = "us-east-1c"
  cidr_block        = "10.0.3.0/24"
  vpc_id            = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-subnet-1c"
  }
}

resource "aws_internet_gateway" "flask_app_igw" {
  vpc_id = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-igw"
  }
}

resource "aws_route_table" "flask_app_route_table" {
  vpc_id = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-route-table"
  }
}

resource "aws_route" "flask_app_route_igw" {
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.flask_app_igw.id
  route_table_id         = aws_route_table.flask_app_route_table.id
}
#routes
#security-groups
#task-definition
#ecs-service
