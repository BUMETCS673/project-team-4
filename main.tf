###################
## VPC Resources ##
###################

resource "aws_vpc" "ecs_cluster_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "ecs-cluster-vpce"
  }
}