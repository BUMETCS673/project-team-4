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

resource "aws_ecs_task_definition" "flask_app_container_td" {
  cpu                = 256
  memory             = 512
  execution_role_arn = "arn:aws:iam::622508827640:role/ecsTaskExecutionRole"
  family             = "flask-app"
  network_mode       = "awsvpc"
  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  requires_compatibilities = ["FARGATE"]
  container_definitions = jsonencode([
    {
      name  = "flask-app"
      image = "nginx:latest"

      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}

resource "aws_ecs_service" "flask_app_svc" {
  name             = "flask-app-svc"  
  cluster          = aws_ecs_cluster.flask_cluster.id
  desired_count    = 1
  launch_type      = "FARGATE"
  
  task_definition = aws_ecs_task_definition.flask_app_container_td.arn

  network_configuration {
    assign_public_ip = "true"
    #security_groups = ""    
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



##############################
## Security Group Resources ##
##############################

resource "aws_security_group" "flask_app_sg" {
  description = "placeholder"
  name        = "placeholder"
  vpc_id      = aws_vpc.flask_app_vpc.id
}

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

#security-groups
#ecs-service
