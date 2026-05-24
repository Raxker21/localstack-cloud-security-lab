Write-Host "Setting up LocalStack Cloud Security Lab..."

$Profile = "localstack"

# Create buckets
aws s3 mb s3://company-public-files --profile $Profile 2>$null
aws s3 mb s3://internal-security-logs --profile $Profile 2>$null

# Create local test files
"Hello from LocalStack S3" | Out-File -Encoding ascii test-file.txt
"2026-05-01 user=admin action=login result=success" | Out-File -Encoding ascii security-log.txt

# Upload test files
aws s3 cp test-file.txt s3://company-public-files/test-file.txt --profile $Profile
aws s3 cp security-log.txt s3://internal-security-logs/security-log.txt --profile $Profile

# Apply public read policy to company-public-files
aws s3api put-bucket-policy `
  --bucket company-public-files `
  --policy file://public-read-policy.json `
  --profile $Profile

# Enable encryption for internal-security-logs
aws s3api put-bucket-encryption `
  --bucket internal-security-logs `
  --server-side-encryption-configuration file://s3-encryption-config.json `
  --profile $Profile

# Keep company-public-files without default encryption for the lab finding
aws s3api delete-bucket-encryption `
  --bucket company-public-files `
  --profile $Profile 2>$null

Write-Host ""
Write-Host "Buckets:"
aws s3 ls --profile $Profile

Write-Host ""
Write-Host "company-public-files policy:"
aws s3api get-bucket-policy --bucket company-public-files --profile $Profile

Write-Host ""
Write-Host "internal-security-logs encryption:"
aws s3api get-bucket-encryption --bucket internal-security-logs --profile $Profile

Write-Host ""
Write-Host "Lab setup completed."