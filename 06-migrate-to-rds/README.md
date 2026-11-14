# Migrate a Café Database to Amazon RDS

I took a café ordering website whose database lived on the same server as the web app and moved the database to a managed Amazon RDS MariaDB instance. Then I pointed the app at the new database without touching its code.

## The idea in plain words

Imagine a café where the owner keeps the order notebook in the same drawer as the cash register. If the shop burns down, you lose both. Moving the notebook to a bank vault is safer, and the bank does the backups for you. That is what RDS is: a database that AWS runs, patches and backs up for you, instead of one you babysit on your own server.

## Architecture

- **Before:** one EC2 instance (CafeInstance) running the web app and the MariaDB database together in a public subnet.
- **After:** CafeInstance still runs the web app. The database lives on an RDS instance in two private subnets that have no route to the internet. Only the web server is allowed to talk to it.

## What I built

1. **Database security group** (`CafeDatabaseSG`): allows MariaDB traffic (port 3306) only from the café web server's security group. See `images/a01` and `a02`.
2. **Two private subnets** in two different Availability Zones, one for each of the database's possible homes. See `images/a03` and `a04`.
3. **DB subnet group**: tells RDS which subnets it may place the database in. RDS requires subnets in at least two AZs even for a single instance. See `images/a05`.
4. **RDS MariaDB instance** `CafeDBInstance`: `db.t3.micro`, 20 GB, not publicly accessible, in the Cafe VPC. See `images/b02`.
5. **Migration**: `mysqldump` the old database to a file, then load that file into RDS with `mysql` over an encrypted (TLS) connection using the Amazon RDS CA bundle.
6. **Cutover**: changed the `/cafe/dbUrl` parameter in Systems Manager Parameter Store from the local server name to the RDS endpoint. The app reads its database address from Parameter Store, so no code changed. See `images/c01`.
7. **Verification**: the order history page still showed the two orders I had placed before the migration, and a new order placed afterwards saved correctly.
8. **Monitoring**: looked at the instance's CloudWatch metrics (CPU, connections, free storage, memory, IOPS). See `images/c02`.

## Key commands

```bash
# on the café web server: back up the old database
mysqldump --user=root -p --databases cafe_db --add-drop-database > cafedb-backup.sql

# download the Amazon RDS certificate bundle so the connection can be encrypted
curl -o global-bundle.pem https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem

# restore into RDS over TLS
mysql --user=root -p --host=<RDS endpoint> --ssl-ca=./global-bundle.pem < cafedb-backup.sql
```

Creating the instance with the CLI:

```bash
aws rds create-db-instance \
  --db-instance-identifier CafeDBInstance \
  --engine mariadb --engine-version 10.11.13 \
  --db-instance-class db.t3.micro --allocated-storage 20 \
  --availability-zone us-west-2a \
  --db-subnet-group-name "CafeDB Subnet Group" \
  --vpc-security-group-ids <CafeDatabaseSG id> \
  --no-publicly-accessible \
  --master-username root --master-user-password '<password>'
```

## Problems I hit and how I fixed them

| Problem | Cause | Fix |
|---|---|---|
| Creating the database in the console failed with "not authorized to perform rds:CreateDBInstance" (tried several settings: engine version, encryption off, 1 day backups, gp2 storage) | The lab's permissions only allowed the exact request the CLI command makes | Created it from the CLI on a helper instance instead |
| CLI said `Cannot find version 10.11.11 for mariadb` | AWS retires old minor versions | Used `10.11.13`, a version that currently exists |
| `Credentials do not match current AWS Account` | A stale console login from an earlier lab | Logged out of the console and opened it again from the lab page |

## Security notes

- The database has no public IP and sits in private subnets. Its security group only accepts traffic from the web server's group, not from IP addresses.
- The connection to RDS uses TLS with the AWS CA bundle.
- Passwords here are placeholders. A real setup would keep them in Secrets Manager or Parameter Store as secure strings and never on the command line.
- Screenshots have account IDs and email addresses blacked out.

## What I learned

- A managed database is mostly about moving responsibility (patching, backups, failover) to AWS.
- Subnet groups, security groups and private subnets are what make a database reachable by the app and nobody else.
- Storing configuration (the database address) in Parameter Store let me switch databases with zero code changes.
- IAM permissions can restrict not just *what* you do but *how* you do it, so "access denied" is worth reading closely.
