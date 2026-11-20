# EBS Snapshot Automation and S3 Versioning

Automated backups for an EC2 instance's disk, with a retention script, then used the AWS CLI to sync files to a versioned S3 bucket and recover a deleted file.

## What I built

- An S3 bucket (versioning enabled) in the console
- An IAM instance profile attached to a running instance so it can call AWS without any stored keys
- A snapshot of the `Processor` instance's EBS volume, taken while the instance was stopped
- A cron job taking a snapshot every minute, then a retention script that keeps only the 2 newest
- An S3 sync workflow with a delete, followed by a recovery from the object version history

## Architecture

A "Command Host" instance (the one I typed commands on) manages a second instance called "Processor" and its EBS volume. Snapshots are stored in S3 behind the scenes, and a separate S3 bucket holds my synced files.

## Steps

1. **Bucket.** Created a general purpose S3 bucket with default settings.
2. **Permissions.** Attached the pre-built `S3BucketAccess` role to Processor (Actions, Security, Modify IAM role). An instance role gives temporary credentials automatically, so nothing secret sits on the box.
3. **Connect.** Used EC2 Instance Connect (browser SSH) to the Command Host.
4. **Initial snapshot.** Looked up Processor's volume ID with `aws ec2 describe-instances`, stopped the instance (`stop-instances` then `wait instance-stopped`) so the disk was consistent, ran `create-snapshot`, waited with `wait snapshot-completed`, and started the instance again.
5. **Scheduled snapshots.** Wrote a crontab entry `* * * * *` that runs `aws ec2 create-snapshot` every minute and logs to `/tmp/cronlog`. After a few minutes `describe-snapshots` showed four snapshots for the volume (1 manual and 3 from cron).
6. **Retention.** Removed the cron job with `crontab -r`. Read `snapshotter_v2.py` (a boto3 script that snapshots each volume and deletes everything older than the newest `MAX_SNAPSHOTS = 2`) and ran it. It printed three `Deleting snapshot` lines and `describe-snapshots` then listed exactly 2 IDs.
7. **S3 sync and versioning.**
   - Downloaded the sample `files` folder (file1, file2, file3) and enabled versioning with `put-bucket-versioning`
   - `aws s3 sync files s3://<bucket>/files/` uploaded all three
   - Deleted `file1.txt` locally and ran `sync --delete`, which removed it from the bucket
   - `list-object-versions` showed the old `file1.txt` version still stored (`IsLatest: false`) under a new delete marker (`IsLatest: true`)
   - Pulled it back with `get-object --version-id`, then ran `sync` again and `file1.txt` (30318 bytes) was back in the bucket

## Verification

- `describe-snapshots` after the script: two snapshot IDs only
- `get-bucket-versioning`: `Enabled`
- Final `aws s3 ls`: file1, file2 and file3 all present

## What I learned

- Stop the instance before snapshotting when you want a clean, consistent disk image.
- Snapshots pile up fast and cost money, so a retention rule matters as much as the backup itself.
- Versioning means "delete" in S3 only adds a delete marker. The real data stays recoverable until you delete a specific version.
- `sync --delete` mirrors deletions, so it is easy to wipe things by accident without versioning on.
- Instance roles beat access keys on servers.

## Notes and honesty

- Terminal output was captured as text, no screenshots saved for this one.
- The snapshots the script deleted were the throwaway ones I created in this lab, as the lab instructs.
- Account, volume and snapshot IDs are left out on purpose. The lab environment is deleted when the session ends.
