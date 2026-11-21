# EC2 Tagging and Resource Management

Used tags to find, update and control groups of EC2 instances, then audited the fleet for instances that break a "tag or terminate" rule.

## What I built

A tag-driven workflow on a small fleet of 9 EC2 instances split across three environments:

| Tag | Purpose |
|---|---|
| `Project` | Which project the instance belongs to (ERPSystem or another) |
| `Environment` | production, staging or development |
| `Version` | Software version of the project (started at 1.0) |

## Steps

1. **Find by tag.** Filtered the instance list with two tag filters at once (`Project = ERPSystem` and `Environment = development`). Exactly 2 instances matched (an app server and a web server).
2. **Bulk update a tag.** Changed `Version` from `1.0` to `1.1` on both matching instances and confirmed on each Tags tab that the new value stuck.
3. **Stop and start by tag.** Stopped both development instances together, confirmed both showed `Stopped`, then started them again and confirmed they went `Pending` then running.
4. **Audit for untagged instances.** Counted instances per `Environment` value: production 2, staging 3, development 2. That is 7 of the 9, so 2 instances have no `Environment` tag at all (one is the management host, plus one more workload instance). Those are the ones a "tag-or-terminate" policy would target.

## Why tags matter

Tags are labels you attach to AWS resources. They turn "a pile of servers" into groups you can act on: stop everything in dev at night to save money, find everything for one project for billing, or flag anything missing an owner for review. A tag policy only works if you can query resources by tag, which is exactly what the filters above do.

## What I learned

- Multiple tag filters combine as AND, so you can narrow to a precise group.
- Changing a tag is instant and does not touch the running instance.
- Stopping and starting by tag is only safe if tags are accurate, so a missing or wrong tag is a real operational risk.
- The EC2 console cannot bulk-edit tags on several instances from the instance list ("Manage tags" is greyed out when more than one is selected), so I edited them one at a time.

## Notes and honesty

- The original lab does this from a command line on a management instance (AWS CLI queries, a tag-changing shell script, and a PHP stop/start script). In my lab environment the browser SSH session, Session Manager and CloudShell were all blocked by the lab's permissions, so I could not run those scripts. I did the same operations (filter by tags, change a tag, stop and start by tag) through the EC2 console instead.
- I did not terminate the untagged instances. They were pre-existing lab resources and I did not want to delete things I had not created, so the audit stops at identifying them.
- No screenshots were saved for this lab. Instance IDs and account details are left out on purpose.
