# LocalStack Cloud Security Lab

## Overview

This project is a hands-on Cloud Security Lab buit with LocalStack, AWS CLI and Pythone

The goal of this lab is to practice basic cloud security concepts without using a real AWS account.
The project demonstrates how an S3 bucket can be misconfigured with public read access and how to detect this issue using Python and boto3.

## Lab Architecture

```text
Local Machine
    |
    | AWS CLI / boto3
    v
LocalStack
    |
    v
S3 Buckets
    |
    v
Python Security Checker
```

## Security Scenario

In this lab, two S3 buckets are created:

- `company-public-files`
- `internal-security-logs`

The `company-public-files` bucket is intentionally configured with a oublic read bucket policy.

The risky part of the policy is:

```json
"Principal": "*",
"Action": "s3:GetObject"
```
This means that anyone can read objects from the bucket.

From a Cloud Security perspective, this is a HIGH severity finding because sensitive files could be exposed if they are uploade to this bucket.

## What Was Implemented

This lab includes:
* LocalStack setup
* AWS CLI profile for LocalStack
* S3 bucket creation
* Test file upload to S3
* Public read bucket policy
* Python script using boto3
* Automatic detection of public S3 bucket read access
* Summary output for HIGH, OK and ERROR checks
* Notes with commands and explanations

### Security Check

The Python script checks S3 bucket policies and detects public read access.

The script looks for the following combination:

```text
Effect: Allow
Principal: *
Action: s3:GetObject
```
It also supports different policy formats, for example:
```json
"Action": "s3:GetObject"
```
and:
```json
"Action": ["s3:GetObject", "s3:ListBucket"]
```
## Example Output

```text
Bucket: company-public-files
[HIGH] Bucket company-public-files allows public read access

Bucket: internal-security-logs
[OK] Bucket internal-security-logs has no bucket policy

Summary:
HIGH findings: 1
OK checks: 1
ERROR checks: 0
```

## How to Run

Start LocalStack:
```bash
localstack start -d
```

Check that LocalStack is running:
```bash
docker ps
```

List S3 buckets:
```bash
aws s3 ls --profile localstack
```

Run the public read checker:
```bash
python scripts/check_s3_public_read.py
```

## Project Structure
```text
localstack-cloud-security-lab/
├── notes/
│   ├── commands.md
│   ├── 01-s3-basics.md
│   └── 02-python-boto3.md
├── scripts/
│   ├── list_s3_buckets.py
│   ├── get_s3_bucket_policies.py
│   └── check_s3_public_read.py
├── public-read-policy.json
├── test-file.txt
├── security-log.txt
├── .gitignore
└── README.md
```
## Skills Practiced

* Cloud Security basics
* S3 bucket security
* Bucket policy analysis
* Public access detection
* AWS CLI basics
* Python boto3 automation
* Error handling with boto3 `ClientError`
* Security findings and summary reporting
* Git and GitHub workflow

## Security Finding

### HIGH: Public S3 Bucket Read Access

The bucket `company-public-files` allows public read access through its bucket policy.

Risk:

Sensitive data could be exposed
Internal files could become publicly readable
Security logs or backups could be leaked if uploaded to the wrong bucket

Recommendation:

Remove public read access unless it is explicitly required
Avoid using `Principal: "*"` with `s3:GetObject`
Keep internal buckets private
Regularly audit bucket policies

## Notes

This project uses LocalStack and does not connect to a real AWS account.

The credentials used in the scripts are test credentials for LocalStack only:

```text
aws_access_key_id = test
aws_secret_access_key = test
```

Do not use real AWS access keys in source code.

## Next Steps

Planned improvements:

* Add JSON report export
* Add CSV report export
* Add S3 encryption checks
* Add IAM policy checks
* Add EC2 security group checks
* Add GitHub Actions
* Add Terraform-based lab setup