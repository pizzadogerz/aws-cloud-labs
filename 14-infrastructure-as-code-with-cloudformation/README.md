# Infrastructure as Code with AWS CloudFormation

Deployed a VPC from a template, then evolved the same stack by editing the template to add an S3 bucket and an EC2 instance, and finally tore everything down in one action.

## What I built

A single CloudFormation stack named `Lab` that grew in three steps:

| Step | Resources in the stack |
|---|---|
| 1. Create | VPC, public subnet, internet gateway, route table and route, security group |
| 2. Update | + an S3 bucket |
| 3. Update | + an EC2 instance (t3.micro, "App Server") placed in the public subnet with the stack's security group |

## How CloudFormation works (the short version)

A template is a text file (YAML) that describes the infrastructure you want. You hand it to CloudFormation and it builds everything in the right order. Change the file, hand it over again, and CloudFormation works out the difference (a "change set") and only adds, changes or removes what is needed. Deleting the stack deletes everything it built.

A template has three main parts:

- **Parameters**: inputs you can change without editing the template (I used CIDR ranges and an AMI lookup)
- **Resources**: the actual infrastructure
- **Outputs**: values the stack reports back

## Steps

1. **Create the stack** from the lab's starter template (via its S3 URL) with default parameters. All 9 resources reached `CREATE_COMPLETE`.
2. **Add an S3 bucket.** Opened the stack's template in the console's template studio and added a two-line resource under `Resources:`:
   ```yaml
   S3Bucket:
     Type: AWS::S3::Bucket
   ```
   Validated it, saved, and let CloudFormation build the change set. The preview showed exactly one change: **Add S3Bucket**. After the update the bucket appeared in the Resources tab with a CloudFormation generated name (no name given, so no naming collisions).
3. **Add an EC2 instance.** Added a parameter that looks up the latest Amazon Linux AMI from Systems Manager Parameter Store, then a new resource that references other resources in the template with `!Ref`:
   ```yaml
   AppServer:
     Type: AWS::EC2::Instance
     Properties:
       ImageId: !Ref AmazonLinuxAMIID
       InstanceType: t3.micro
       SecurityGroupIds:
         - !Ref AppSecurityGroup
       SubnetId: !Ref PublicSubnet
       Tags:
         - Key: Name
           Value: App Server
   ```
   The change set again showed a single **Add** (AppServer, `AWS::EC2::Instance`) and the stack finished `UPDATE_COMPLETE`.
4. **Tear down.** Deleted the stack. CloudFormation removed every resource it created in dependency order (instance first, then subnet and route table, VPC last).

## What I learned

- Infrastructure described as code is repeatable: the same file produces the same VPC every time.
- The change set preview is a safety net. It shows what will be added, modified or replaced before anything happens.
- `!Ref` is how resources connect to each other, so I never hard-code IDs.
- Using a Parameter Store lookup for the AMI avoids hard-coding region specific image IDs.
- YAML indentation is part of the syntax. Mixed up spaces break the template, which is why validating first matters.
- Tearing down with one click is a cost-control and security win compared with hunting resources by hand.

## Notes and honesty

- The lab has you download the template and upload an edited file. In my setup I created the stack straight from the template's S3 URL and made the edits in the console's template studio instead, since I could not upload a local file. The resulting templates match what the lab asks for.
- Saving from template studio stores the template in a CloudFormation-managed S3 bucket. That bucket is not part of the stack and was left alone.
- No screenshots were saved for this lab. Account and resource IDs are left out on purpose.
