##################
## Account Data ##
##################

data "aws_region" "current" {}

##################
## VPC Data ##
##################




data "aws_route53_zone" "bum_tv" {
  name         = "bumtelevision.com"
  private_zone = false
}