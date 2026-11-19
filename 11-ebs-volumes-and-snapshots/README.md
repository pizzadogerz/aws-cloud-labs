# EBS Volumes and Snapshots

Created a new disk (EBS volume), attached it to a running Linux server, formatted and mounted it, backed it up with a snapshot, then restored the snapshot to a second disk to prove a deleted file comes back.

## The idea (newbie version)

An EC2 instance is like a computer, and **EBS** is its hard drive that lives separately from the computer. That separation is the point:

- You can plug in extra drives (attach a volume), or unplug them.
- A **snapshot** is a backup photo of the drive. Only the used parts are stored, so it is cheap.
- A **restore** is making a brand new drive from that photo.

## What I did

1. **Created a volume**: General Purpose SSD (gp2), 1 GiB, in the **same Availability Zone** as the server (`us-west-2a`), tagged `Name = My Volume`. A volume can only attach to an instance in its own AZ, like a USB stick that only fits the computer in the same room.
2. **Attached it** to the `Lab` instance as `/dev/sdb`.
3. **Formatted and mounted it** from the instance terminal (EC2 Instance Connect in the browser):

```bash
sudo mkfs -t ext3 /dev/sdb                 # put an ext3 file system on the blank disk
sudo mkdir /mnt/data-store                 # create a folder to use as the mount point
sudo mount /dev/sdb /mnt/data-store        # plug the disk into that folder
echo "/dev/sdb   /mnt/data-store ext3 defaults,noatime 1 2" | sudo tee -a /etc/fstab   # remount on reboot
df -h                                      # confirm
```

`df -h` then showed the new disk (the OS names it `/dev/nvme1n1` on this instance type) with about 975 MB and mounted at `/mnt/data-store`.

4. **Wrote a file** to it and read it back:

```bash
sudo sh -c "echo some text has been written > /mnt/data-store/file.txt"
cat /mnt/data-store/file.txt
# some text has been written
```

5. **Took a snapshot** of `My Volume`, tagged `My Snapshot`. It went from Pending to Completed, and the full snapshot size was only **53 MiB** for a 1 GiB volume, because only used blocks are copied.
6. **Deleted the file** on the server to simulate a mistake:

```bash
sudo rm /mnt/data-store/file.txt
ls /mnt/data-store/file.txt
# ls: cannot access /mnt/data-store/file.txt: No such file or directory
```

7. **Restored the snapshot** into a new 1 GiB volume (`Restored Volume`, same AZ), attached it as `/dev/sdc`, mounted it somewhere else, and the file was back:

```bash
sudo mkdir /mnt/data-store2
sudo mount /dev/sdc /mnt/data-store2
ls /mnt/data-store2/file.txt
# /mnt/data-store2/file.txt
cat /mnt/data-store2/file.txt
# some text has been written
```

## Key concepts

| Term | Plain meaning |
|---|---|
| EBS volume | A network-attached hard drive for EC2 |
| Availability Zone match | A volume only attaches to instances in the same AZ |
| Snapshot | A point-in-time backup stored in S3, incremental, so only changed blocks cost anything |
| Restore | Create a new volume from a snapshot, even in another AZ |
| `fstab` | The file that tells Linux which disks to mount at boot |

## Notes

- I did not keep screenshots for this lab. My screenshot capture stopped saving files during the session, so the terminal output above (copied from the terminal itself) is the evidence instead.
- I stopped after the restore. Volumes and snapshots keep costing money until deleted, but the lab environment cleans everything up when the lab ends, so I left them for the cleanup. In a real account you would delete the test volumes and snapshot.
- The restore page showed a "not authorized" note for the Fast Snapshot Restore feature. The lab permissions block that option, and the normal restore worked fine without it.

## What I learned

Separating storage from compute is what makes backups and recovery easy. A snapshot is how you protect the data on a volume, and restoring is just creating a new volume from it.
