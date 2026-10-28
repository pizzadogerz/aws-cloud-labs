# AWS Cloud Labs

Hands-on labs from the AWS re/Start program. Each lab has the steps I followed, screenshots, and what I learned.

## Skills practiced
- AWS CLI and IAM
- EC2 instances, AMIs and SSH
- VPC networking: subnets, route tables, internet gateways and security groups
- Load balancing and Auto Scaling
- High availability with Route 53 health checks and failover
- CloudWatch alarms
- S3 static website hosting
- Linux command line
- Bash scripting basics and troubleshooting

## Labs

| # | Lab | What I did |
|---|-----|------------|
| 01 | [Install and Configure the AWS CLI](./01-install-configure-aws-cli) | Installed the CLI on an EC2 instance, configured it with an access key, and pulled an IAM policy from the terminal |
| 02 | [Host a Static Website on S3](./02-s3-static-website) | Created an S3 bucket and an IAM user from the CLI, hosted a café website from the bucket, and automated updates with a script |
| 03 | [Amazon EC2 Instances](./03-ec2-instances) | Launched a bastion host and web servers from the console and CLI, built a VPC from scratch, and fixed a launch script with two hidden bugs |
| 04 | [Scaling and High Availability](./04-scaling-and-high-availability) | Put servers behind an Application Load Balancer, scaled them automatically with Auto Scaling, and set up Route 53 failover to a backup server |

## About
Career shifter from mechanical engineering into cloud, building hands-on experience through the AWS re/Start program.
