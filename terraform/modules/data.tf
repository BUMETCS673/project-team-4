##################
## Account Data ##
##################

data "aws_region" "current" {}

##################
## VPC Data ##
##################

data "aws_route_table" "selected" {
  vpcvpc_id = aws_vpc.flask_vpc.id

  tags = {
    Name = "flask-app-rt"
  }
}