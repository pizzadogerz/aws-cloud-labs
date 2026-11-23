# CloudFormation: VPC with a Private Subnet and EC2 Instance

## Overview
A challenge-style project: build a small network and a server from scratch as code, with no step-by-step instructions. The requirement was one CloudFormation template that creates a VPC, an internet gateway attached to it, a security group allowing SSH, a private subnet, and a t3.micro EC2 instance in that private subnet.

Think of CloudFormation as a blueprint for a building. You describe the rooms (VPC, subnet, server) in a file, hand it to AWS, and AWS builds all of it in the right order.

## What I Built
| Resource | Type | Notes |
|---|---|---|
| Challenge VPC | `AWS::EC2::VPC` | 10.1.0.0/16, DNS support and hostnames on |
| Challenge IGW | `AWS::EC2::InternetGateway` | The VPC's door to the internet |
| IGWAttachment | `AWS::EC2::VPCGatewayAttachment` | Attaches the gateway to the VPC |
| Private Subnet | `AWS::EC2::Subnet` | 10.1.2.0/24 |
| SSHSecurityGroup | `AWS::EC2::SecurityGroup` | Inbound TCP 22 from 0.0.0.0/0 |
| Private Instance | `AWS::EC2::Instance` | t3.micro, in the private subnet |

The AMI is not hard coded. A parameter of type `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>` points at the public SSM path for the latest Amazon Linux 2 image, so the template keeps working as images get updated.

## Steps
1. Opened CloudFormation, chose Create stack, then "Build with template studio".
2. Wrote the template as JSON in the studio editor (JSON is valid for CloudFormation, and it avoided indentation problems in the browser editor).
3. Used Validate. The first attempt failed with "End of file expected" because the editor had added an extra closing brace. Removing it fixed validation, and the diagram view then showed the resources and their links.
4. Saved the template, named the stack `Challenge`, kept the default parameter, and submitted.
5. Watched the Events tab until every resource reached `CREATE_COMPLETE` and the stack itself reported `CREATE_COMPLETE`.

## What I Learned
- Resources reference each other with `Ref`, and CloudFormation works out the build order from those references (the gateway attachment waits for the VPC and gateway, the instance waits for the subnet and security group).
- Template studio validates before you deploy, which catches syntax mistakes early.
- Pulling the AMI from an SSM parameter beats copying an AMI ID that is only valid in one region and goes stale.
- "Private" subnet here means no route to the internet gateway was added. A subnet is only public if its route table points at the gateway.

## Notes and Honesty
- The security group allows SSH from anywhere because the challenge asked for it. That is not good practice for a real environment, where SSH should be limited to a known IP range or replaced with Session Manager.
- I did not SSH into the instance (not required, and the instance sits in a private subnet anyway).
- The challenge says to let the instructor know when done, so verification here is only my own check of the stack status and events.
- The stack and its resources were left for the lab teardown to remove. The template was saved to the account's auto-created `cf-templates` bucket, which I left alone.

## Skills Demonstrated
CloudFormation, infrastructure as code, VPC networking basics, security groups, template validation and troubleshooting.
