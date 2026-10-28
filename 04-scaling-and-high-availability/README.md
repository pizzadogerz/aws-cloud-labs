# Scaling and High Availability

Hands-on labs about keeping a web app online and able to handle traffic spikes or failures on AWS. There are three parts. Each has the steps I followed, screenshots, and what I learned.

## Part 1: Load balancing and auto scaling (console)

### Goal
Start with one web server and turn it into a setup that spreads traffic across several servers in two Availability Zones, then adds or removes servers automatically as CPU load changes.

Starting point: one web server (Web Server 1) in a public subnet.
End result: an Application Load Balancer in the public subnets sending traffic to an Auto Scaling group of servers in the private subnets.

### What I did

**1. Made an AMI from the existing server.** An AMI is a saved copy of a server's disk, so new servers can be launched with the same content. I created one from Web Server 1 called `Web Server AMI`.

![Create image form](screenshots/01-create-ami.png)

The AMI sat in Pending for a while. When I refreshed the AMIs page it showed Available (the page does not refresh itself).

![AMI available](screenshots/02-ami-available.png)

**2. Created the load balancer.** The load balancer is the single front door that hands each visitor to a healthy server. I made an internet facing Application Load Balancer named `LabELB` in the Lab VPC, mapped to both public subnets (one per Availability Zone).

![Load balancer configuration](screenshots/03-alb-config.png)

I removed the default security group and attached only the Web Security Group, which allows HTTP.

![Security group](screenshots/04-alb-security-group.png)

Then I created a target group called `lab-target-group` (target type Instances) and set the HTTP:80 listener to forward to it.

![Listener forwarding to the target group](screenshots/05-alb-listener.png)

![Load balancer created](screenshots/06-alb-created.png)

**3. Created a launch template.** This is the recipe the Auto Scaling group uses to launch each new server: which AMI, which instance type, which security group. I used `Web Server AMI`, `t3.micro`, no key pair, and the Web Security Group.

![Launch template settings](screenshots/07-launch-template.png)

![Launch template network settings](screenshots/08-launch-template-network.png)

![Launch template created](screenshots/09-launch-template-created.png)

**4. Created the Auto Scaling group.** I named it `Lab Auto Scaling Group` and pointed it at the launch template.

![Name and launch template](screenshots/10-asg-name-template.png)

The servers go in the two private subnets (10.0.1.0/24 and 10.0.3.0/24), so they are not directly reachable from the internet.

![Private subnets](screenshots/11-asg-network.png)

I attached the group to the existing load balancer target group and turned on ELB health checks, so a server that stops answering gets replaced.

![Attached to the load balancer](screenshots/12-asg-load-balancing.png)

Group size is desired 2, minimum 2, maximum 4, with a target tracking policy that keeps average CPU at 50 percent.

![Group size and scaling policy](screenshots/13-asg-size-scaling.png)

I added a `Name = Lab Instance` tag, reviewed everything, and created the group.

![Review page](screenshots/14-asg-review.png)

![Auto Scaling group created](screenshots/15-asg-created.png)

**5. Checked that it worked.** The group launched two `Lab Instance` servers, one in each Availability Zone.

![Two instances in two zones](screenshots/16-two-instances.png)

Both showed up as healthy in the target group, which means the load balancer is willing to send traffic to them.

![Healthy targets](screenshots/17-targets-healthy.png)

Opening the load balancer's DNS name in a browser loaded the Load Test app. It shows which instance and which zone served my request.

![Load Test app](screenshots/19-load-test-app.png)

**6. Tested auto scaling.** The group created two CloudWatch alarms on its own. Before the test, AlarmHigh (CPU above 50 percent) was OK.

![Alarms before the test](screenshots/20-alarms-ok.png)

I clicked Load Test in the app, which pushes the server's CPU up.

![Load test running at 72 percent CPU](screenshots/21-load-test-running.png)

After a few minutes of CPU above 50 percent, AlarmHigh went to In alarm.

![AlarmHigh in alarm](screenshots/22-alarmhigh-in-alarm.png)

Auto Scaling responded by launching extra servers beyond the original two.

![More instances launched](screenshots/23-more-instances.png)

**7. Cleaned up.** Web Server 1 was only needed to create the AMI, so I terminated it.

![Web Server 1 terminated](screenshots/24-web-server-terminated.png)

### Troubleshooting
- **The site timed out.** Opening the load balancer DNS name gave `ERR_TIMED_OUT`. My browser had switched to https, and the load balancer only has an HTTP listener on port 80. Typing `http://` in front of the DNS name fixed it.

![Timeout error](screenshots/18-https-timeout.png)

- **Wrong security group on the load balancer.** After removing the default security group and adding the Web Security Group, both were selected. I removed `default` so only the Web Security Group stayed.
- **AMI looked stuck on Pending.** It was just a stale page. Refreshing the AMIs page showed Available.

### Security note
Only the load balancer faces the internet. The servers sit in private subnets and only receive traffic through the load balancer. This is the usual pattern for production web apps because it keeps the servers off the public internet. The lab environment and its resources were deleted when the lab ended.

### What I learned
I learned how a load balancer and an Auto Scaling group work together: the load balancer spreads traffic and checks server health, and the Auto Scaling group keeps the right number of servers running. I saw that a launch template is just a saved recipe for new servers, and that target tracking scaling uses CloudWatch alarms behind the scenes to add servers when CPU stays high. I also learned that putting servers in private subnets behind a load balancer keeps them off the public internet.

## Part 2: Auto scaling from the command line and console

### Goal
Do the same kind of setup as Part 1, but this time build most of it from the AWS CLI (the command line) instead of clicking through the console. Then prove it works by stressing the servers and watching the group grow.

I worked from a "Command Host", a small server whose job is to run AWS CLI commands. It uses an IAM role, so I did not have to type any access keys.

### What I did

**1. Pointed the CLI at the right Region and checked who I was.** I set the Region to `us-west-2` and ran `aws sts get-caller-identity` to confirm the CLI was using the lab role.

![Setting the Region](screenshots/25-cli-region-configure.png)

![CLI identity](screenshots/26-cli-configure-identity.png)

**2. Found the user data script.** User data is a script a server runs the first time it boots. Mine installs and starts the web app. My first attempt failed because I typed `userdata.txt`, but the file is `UserData.txt`. Linux file names are case sensitive.

![File not found](screenshots/27-userdata-not-found.png)

![Finding the file](screenshots/28-find-userdata.png)

![Contents of the script](screenshots/29-userdata-contents.png)

**3. Launched a web server from the CLI.** I stored the values I kept needing (key name, AMI, security group, subnet) in shell variables so I did not have to retype long IDs, then ran `aws ec2 run-instances` with the user data script and tagged it `webserver`.

![Variables](screenshots/30-variables.png)

![run-instances](screenshots/31-run-instances.png)

![Server running](screenshots/32-server-running.png)

A quick `curl` returned HTTP 200, so the web app was up.

![Web server answers with 200](screenshots/33-web-server-http-200.png)

**4. Saved it as an image.** `aws ec2 create-image` made an AMI called `webserverAMI` from that server.

![create-image](screenshots/34-create-image.png)

**5. Built the load balancer pieces from the CLI.** I looked up the VPC and subnet IDs, then created a target group `webserver-app` (health check path `/index.php`), an Application Load Balancer `WebServerELB` across the two public subnets, and an HTTP:80 listener that forwards to the target group.

![VPC and subnet variables](screenshots/35-vpc-subnet-variables.png)

![Load balancer, target group and listener](screenshots/36-alb-target-group-listener.png)

**6. Created a launch template.** Once the AMI showed Available, I made `web-app-launch-template` (t3.micro, the HTTPAccess security group, no key pair) from the CLI.

![AMI available and launch template](screenshots/37-ami-available-launch-template.png)

**7. Created the Auto Scaling group in the console.** I tried the CLI first, but it was denied (see Troubleshooting), so I used the console wizard instead. The group is `Web App Auto Scaling Group`, uses the launch template, and runs in the Lab VPC.

![CLI denied](screenshots/38-asg-cli-access-denied.png)

![Wizard step 1](screenshots/39-asg-wizard-step1.png)

The servers go in the two private subnets (10.0.2.0/24 and 10.0.4.0/24).

![Private subnets](screenshots/40-asg-network.png)

I attached the group to the `webserver-app` target group and turned on ELB health checks.

![Load balancing](screenshots/41-asg-load-balancing.png)

Size is desired 2, minimum 2, maximum 4, with a target tracking policy that keeps average CPU at 50 percent.

![Size and scaling](screenshots/42-asg-size-scaling.png)

![Review](screenshots/43-asg-review.png)

![Group created](screenshots/44-asg-created.png)

**8. Checked that it was healthy.** Two `WebApp` instances launched, and both showed Healthy in the target group.

![Two instances](screenshots/45-two-instances.png)

![Targets healthy](screenshots/46-targets-healthy.png)

**9. Stressed the servers.** The sample app has a Load Test button that burns CPU. Chrome would not open the load balancer address (see Troubleshooting), so I triggered the same thing from the Command Host with `curl`.

![Stress request sent](screenshots/47-stress-sent.png)

AlarmHigh started at OK.

![Alarm OK before the test](screenshots/48-alarm-ok-before.png)

CPU climbed to about 99 percent.

![CPU metrics](screenshots/49-cpu-metrics.png)

After a few minutes AlarmHigh switched to In alarm. These alarms use 5 minute metrics, so it takes around 15 minutes.

![AlarmHigh in alarm](screenshots/50-alarm-in-alarm.png)

The group scaled from 2 servers to 4.

![Four instances](screenshots/51-four-instances.png)

The activity history shows the launches that the alarm triggered.

![Activity history](screenshots/52-activity-history.png)

### Troubleshooting
- **`userdata.txt` not found.** The real name is `UserData.txt`. Linux treats upper and lower case as different.
- **CLI `create-auto-scaling-group` was AccessDenied.** The Command Host role is not allowed to use the launch template this way, so I created the Auto Scaling group in the console, which worked.
- **The wizard picked the wrong VPC.** It defaulted to the default VPC. I switched it to the Lab VPC so the subnets matched.
- **The browser would not load the site.** Chrome showed "This site doesn't support a secure connection" because it tries https first and my load balancer only has HTTP. Using `curl` from the Command Host got around it.
- **The first stress attempt did nothing.** I sent a POST, but the app's button is a GET request (`index.php?stress=start`). Switching to GET worked.

### Security note
The servers are in private subnets and only reachable through the load balancer. I did not type any access keys, because the Command Host uses an IAM role. The lab account and its resources were deleted when the lab ended.

### What I learned
Everything in the console can be done from the CLI, and storing IDs in variables makes long commands manageable. I also learned the CLI role can have fewer permissions than the console, so it is good to know a second route. Watching the alarm fire and the group grow from 2 to 4 servers made target tracking click for me.

## Part 3: Route 53 failover

### Goal
Make a website survive a server failure. Route 53 is AWS's DNS service, the phone book that turns a name like `www` into an IP address. With failover routing, it normally sends people to the primary server, and if a health check says that server is down, it sends them to the backup instead.

### What I did

**1. Started with two servers.** Two Cafe web servers in different Availability Zones. CafeInstance1 (us-west-2a) is the primary and CafeInstance2 (us-west-2b) is the backup.

![Two Cafe instances](screenshots/53-cafe-instances.png)

**2. Created a health check.** A health check is Route 53 knocking on the primary server every so often to see if it answers. I used HTTP to the primary's IP on port 80, path `/cafe`, checked every 10 seconds, and it must fail 2 times in a row to count as unhealthy.

![Health check settings](screenshots/54-health-check-config.png)

![Health check created](screenshots/55-health-check-created.png)

I skipped the optional email alarm.

**3. Created the primary record.** In the hosted zone I made an A record called `www` with the failover policy set to Primary, pointing at CafeInstance1, with the health check attached. TTL is 15 seconds, which is how long other servers may remember the answer, so changes show up quickly.

![Primary record](screenshots/56-primary-record.png)

**4. Created the secondary record.** Same name `www`, failover type Secondary, pointing at CafeInstance2, no health check.

![Secondary record](screenshots/57-secondary-record.png)

![Both records created](screenshots/58-records-created.png)

**5. Tested the normal case.** Route 53 has a Test record tool that shows what it would answer. With the primary healthy it returned the primary's IP.

![Test record returns the primary](screenshots/59-test-record-primary.png)

**6. Broke the primary on purpose.** I stopped CafeInstance1.

![Stopping the primary](screenshots/60-instance1-stopping.png)

After a short wait, the health check turned Unhealthy.

![Health check unhealthy](screenshots/61-health-check-unhealthy.png)

**7. Tested again.** The same test now returned the backup server's IP, so traffic moved over automatically.

![Test record returns the secondary](screenshots/62-test-record-secondary.png)

### Troubleshooting
- **Could not check the site in the browser.** Chrome's https-first warning blocked the plain HTTP site, so I used the Route 53 Test record tool to confirm the answer.
- **Form fields got mixed up.** When I made the secondary record the form layout shifted and I typed `www` into the wrong box. I fixed it by retyping the fields.

### Security note
The records use public IPs because they are public web servers, so the real protection is in the security groups. The lab account and its resources were deleted when the lab ended.

### What I learned
I learned that high availability is not only about more servers, it is also about DNS deciding where to send people. A health check plus a primary and secondary record gives automatic failover with no one touching anything. A low TTL matters too, because a high one would make visitors keep going to a dead server for longer.
