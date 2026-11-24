# AWS Cloud Labs

Hands-on labs from the AWS re/Start program (cohort PHMAN30). Each lab has the steps I followed, what I built, and what I learned, explained in plain words.

I'm a mechanical engineering graduate moving into cloud. My path is Cloud Support first, then Cloud Support Engineer, then cloud security, and I'm preparing for the AWS Certified Cloud Practitioner (CLF-C02) exam. These labs are the hands-on side of that: networking, compute, storage, databases, monitoring, security auditing and infrastructure as code.

## Skills practiced
- AWS CLI and IAM
- EC2 instances, AMIs and SSH
- VPC networking: subnets, route tables, internet gateways and security groups
- Load balancing and Auto Scaling
- High availability with Route 53 health checks and failover
- CloudWatch monitoring: agent, logs, metric filters and alarms
- Serverless with AWS Lambda, S3 triggers, SNS email alerts and EventBridge schedules
- Managed databases with Amazon RDS: subnet groups, security groups, private networking and TLS migration
- Custom VPC networking: subnets, route tables, internet gateway, bastion host and NAT gateway
- Network troubleshooting: route tables, network ACLs and security groups
- Auditing and incident investigation with AWS CloudTrail
- Block storage with Amazon EBS: volumes, file systems, mounts and snapshot restores
- Backup automation with cron and the AWS CLI, plus S3 versioning and object recovery
- Resource tagging: tag filters, tag updates and tag-based audits
- Infrastructure as code with CloudFormation: templates, parameters, change sets, stack updates and teardown
- Building a VPC, private subnet and instance from a single CloudFormation template
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
| 05 | [AWS Lambda](./05-aws-lambda) | Built a scheduled café sales report with Lambda, a layer and SNS, and a word counter that emails the result whenever a text file lands in S3 |
| 06 | [Migrate to Amazon RDS](./06-migrate-to-rds) | Moved a café app database off its web server into a managed RDS MariaDB instance in private subnets, then repointed the app through Parameter Store |
| 07 | [Custom VPC from Scratch](./07-custom-vpc) | Built a VPC with public and private subnets, internet gateway, bastion host and NAT gateway |
| 08 | [Troubleshooting a Broken VPC](./08-troubleshoot-vpc) | Diagnosed an unreachable web server and fixed a missing internet route and a network ACL rule that blocked SSH |
| 09 | [Investigating a Hack with CloudTrail](./09-cloudtrail-investigation) | Enabled a CloudTrail trail and traced a malicious security group change back to the IAM user and source IP |
| 10 | [Monitoring with CloudWatch](./10-cloudwatch-monitoring) | Installed the CloudWatch agent, shipped web logs and memory metrics, and built a metric filter and alarm that fires on repeated 404 errors |
| 11 | [EBS Volumes and Snapshots](./11-ebs-volumes-and-snapshots) | Created, attached, formatted and mounted an EBS volume, snapshotted it, deleted a file, and restored it from the snapshot |
| 12 | [EBS Snapshot Automation and S3 Versioning](./12-ebs-snapshot-automation-and-s3-versioning) | Automated EBS snapshots with cron and a retention script, then synced files to a versioned S3 bucket and recovered a deleted file |
| 13 | [EC2 Tagging and Resource Management](./13-ec2-tagging-and-resource-management) | Filtered instances by multiple tags, bulk-updated a tag, stopped and started a group by tag, and audited for untagged instances |
| 14 | [Infrastructure as Code with CloudFormation](./14-infrastructure-as-code-with-cloudformation) | Built a VPC stack from a template, then updated it to add an S3 bucket and an EC2 instance, and tore it all down with one delete |
| 15 | [CloudFormation VPC and Private Instance](./15-cloudformation-vpc-and-private-instance) | Wrote one template from scratch that builds a VPC, internet gateway, SSH security group, private subnet and EC2 instance |

## Also completed in the course
These were completed through the re/Start platform but are not reproduced as write-ups here:
- Cost and resource utilization activity (reading and analysis, nothing to build)
- Troubleshooting AWS CloudFormation deployments (needed an SSH key file from the lab platform, so I did not reproduce it)
- The remaining knowledge checks and exam prep modules, completed at 100

## About
Career shifter from mechanical engineering into cloud, building hands-on experience through the AWS re/Start program.
