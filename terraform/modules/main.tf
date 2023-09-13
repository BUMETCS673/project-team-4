##############
## TF State ##
##############

#terraform {
#  backend "s3" {
#    bucket = "terraform-state-09-12-2023-bu-cs673"
#    key    = "terraform.tfstate"
#    region = "us-east-1"
#  }
#}

###################
## ACM Resources ##
###################



###################
## ALB Resources ##
###################


##########################
## CloudWatch Resources ##
##########################



###################
## ECS Resources ##
###################

resource "aws_ecs_cluster" "flask_app_cluster" {
  name = "flask-app-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "flask_service" {
  family = "service"
  container_definitions = jsonencode([
    {
      name      = "flask-app"
      image     = "flask-app:latest"
      cpu       = 10
      memory    = 512
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])

  volume {
    name      = "service-storage"
    host_path = "/ecs/service-storage"
  }

  placement_constraints {
    type       = "memberOf"
    expression = "attribute:ecs.availability-zone in [us-east-1a, us-east-1b, us-east-1c]"
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

resource "aws_vpc" "flask_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "flask-app-vpc"
  }
}

resource "aws_subnet" "flask_subnet_1a" {
  availability_zone = "us-east-1a"
  cidr_block        = "10.0.1.0/24"
  vpc_id            = aws_vpc.flask_vpc.id

  tags = {
    Name = "flask-app-subnet-1a"
  }
}

resource "aws_subnet" "flask_subnet_1b" {
  availability_zone = "us-east-1b"
  cidr_block        = "10.0.2.0/24"
  vpc_id            = aws_vpc.flask_vpc.id

  tags = {
    Name = "flask-app-subnet-1b"
  }
}

resource "aws_subnet" "flask_subnet_1c" {
  availability_zone = "us-east-1c"
  cidr_block        = "10.0.3.0/24"
  vpc_id            = aws_vpc.flask_vpc.id

  tags = {
    Name = "flask-app-subnet-1c"
  }
}

resource "aws_internet_gateway" "flask_vpc_igw" {
  vpc_id = aws_vpc.flask_vpc.id

  tags = {
    Name = "flask-app-igw"
  }
}

