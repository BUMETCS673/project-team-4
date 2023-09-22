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
  name          = "flask-app-svc"
  cluster       = aws_ecs_cluster.flask_cluster.id
  desired_count = 1
  launch_type   = "FARGATE"

  task_definition = aws_ecs_task_definition.flask_app_container_td.arn

  network_configuration {
    assign_public_ip = "true"
    #security_groups = ""  
    subnets = [aws_subnet.flask_app_subnet_1a.id]
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



########################
## RDS Resources ##
########################

resource "aws_rds_cluster" "flask_app_db_cluster" {
  cluster_identifier     = "flask-app-db-cluster"
  db_subnet_group_name   = aws_db_subnet_group.flask_app_subnet_group.name
  engine                 = "aurora-mysql"
  engine_mode            = "provisioned"
  engine_version         = "8.0.mysql_aurora.3.02.0"
  database_name          = "test"
  master_username        = "tvbum_admin"
  master_password        = "od9KN7pOhEV32oz"
  vpc_security_group_ids = [aws_security_group.flask_app_sg.id]

  serverlessv2_scaling_configuration {
    max_capacity = 1.0
    min_capacity = 0.5
  }
}

resource "aws_rds_cluster_instance" "flask_app_db" {
  cluster_identifier   = aws_rds_cluster.flask_app_db_cluster.id
  db_subnet_group_name = aws_db_subnet_group.flask_app_subnet_group.name
  identifier           = "flask-app-rds-cluster"
  instance_class       = "db.serverless"
  engine               = aws_rds_cluster.flask_app_db_cluster.engine
  engine_version       = aws_rds_cluster.flask_app_db_cluster.engine_version
  publicly_accessible = true
}

resource "aws_db_subnet_group" "flask_app_subnet_group" {
  name       = "flask-app-subnet-group"
  subnet_ids = [aws_subnet.flask_app_subnet_1a.id, aws_subnet.flask_app_subnet_1b.id, aws_subnet.flask_app_subnet_1c.id, ]

  tags = {
    Name = "flask-app-subnet-group"
  }
}

###############################
## Secrets Manager Resources ##
###############################



##############################
## Security Group Resources ##
##############################

resource "aws_security_group" "flask_app_sg" {
  description = "Security group for flask app rds"
  name        = "flask-app-sg"
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
  map_public_ip_on_launch = true
  vpc_id            = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-subnet-1a"
  }
}

resource "aws_subnet" "flask_app_subnet_1b" {
  availability_zone = "us-east-1b"
  cidr_block        = "10.0.2.0/24"
  map_public_ip_on_launch = true
  vpc_id            = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-subnet-1b"
  }
}

resource "aws_subnet" "flask_app_subnet_1c" {
  availability_zone = "us-east-1c"
  cidr_block        = "10.0.3.0/24"
  map_public_ip_on_launch = true
  vpc_id            = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-subnet-1c"
  }
}

resource "aws_route_table" "flask_app_route_table" {
  vpc_id = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-route-table"
  }
}

resource "aws_route_table_association" "subnet_1a" {
  subnet_id      = aws_subnet.flask_app_subnet_1a.id
  route_table_id = aws_route_table.flask_app_route_table.id
}

resource "aws_route_table_association" "subnet_1b" {
  subnet_id      = aws_subnet.flask_app_subnet_1b.id
  route_table_id = aws_route_table.flask_app_route_table.id
}

resource "aws_route_table_association" "subnet_1c" {
  subnet_id      = aws_subnet.flask_app_subnet_1c.id
  route_table_id = aws_route_table.flask_app_route_table.id
}

resource "aws_internet_gateway" "flask_app_igw" {
  vpc_id = aws_vpc.flask_app_vpc.id

  tags = {
    Name = "flask-app-igw"
  }
}

resource "aws_route" "flask_app_route_igw" {
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.flask_app_igw.id
  route_table_id         = aws_route_table.flask_app_route_table.id
}
