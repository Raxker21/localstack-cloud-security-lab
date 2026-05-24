# Commands

```bash
aws s3 mb s3://company-public-files --profile localstack #создание bucket company-public-files
aws s3 mb s3://internal-security-logs --profile localstack #создание bucket internal-security-logs
aws s3 cp test-file.txt s3://company-public-files/test-file.txt --profile localstack # копирование файлов в bucket
aws s3 cp security-log.txt s3://internal-security-logs/security-log.txt --profile localstack
aws s3 ls --profile localstack # проверка какие bucketы существуют
```

## S3 bucket policy

### Created puclic read policy file

```bash
notepad public-read-policy.json
```

### Applied public read policy to `company-public-files`

```bash
aws s3api put-bucket-policy --bucket company-public-files --policy file://public-read-policy.json --profile localstack
```

### Checked bucket policy for `company-bulic-files`

```bash
aws s3api get-bucket-policy --bucket company-public-files --profile localstack
```

### Checked bucket policy for `internal-security-logs`

```bash
aws s3api get-bucket-policy --bucket internal-security-logs --profile localstack
```

Result `NoSuchBucketPolicy`.
This means no coustom bucket policy os configured for `internal-security-logs`


## Python boto3 setup 

```bash
pip install boto3
python -c "import boto3; print('boto3 installed')"
python scripts\list_s3_buckets.py
```

## Checked S3 bucket policies

```bash
python scripts\get_s3_bucket_policies.py
```

Result:
```text
Bucket: company-public-files
Policy found

Bucket: internal-security-logs
Policy not found
```

## S3 public read check

```bash
python scripts\check_s3_public_read.py
```

Result:
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

## S3 encryption configuration

### Checked bucket encryption

```bash
aws s3api get-bucket-encryption --bucket company-public-files --profile localstack
aws s3api get-bucket-encryption --bucket internal-security-logs --profile localstack
```

### Created encryption configuration

```bash
notepad s3-encryption-config.json
```

### Enabled enryption for internal security logs bucket

```bash
aws s3api put-bucket-encryption --bucket internal-security-logs --server-side-encryption-configuration file://s3-encryption-config.json --profile localstack
```

### Verified encryption 

```bash
aws s3api get-bucket-encryption --bucket internal-security-logs --profile localstack
```

## Recreate LocalStack lab state

If LocalStack state is reset, the lab can be recreated using:

```bash
powershell -ExecutionPolicy Bypass -File .\setup_lab.ps1
```
This script creates the S3 buckets, uploads test files, applies the public read bucket policy and enables default encryption for the internal security logs bucket.