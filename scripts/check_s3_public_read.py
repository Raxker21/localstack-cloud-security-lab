import boto3
import json
from botocore.exceptions import ClientError


def has_get_object_action(action):
    if isinstance (action, str):
        return action == "s3:GetObject"
    if isinstance (action, list):
        return "s3:GetObject" in action
    return False
    
def is_public_principal(principal):
    if principal == "*":
        return True
    if isinstance(principal, dict):
        aws_principal = principal.get("AWS")
        return aws_principal == "*"
    return False

high_count = 0
ok_count = 0
error_count = 0

s3 = boto3.client("s3",
                endpoint_url="http://localhost.localstack.cloud:4566",
                aws_access_key_id="test",
                aws_secret_access_key="test",
                region_name="us-east-1",
                )
response = s3.list_buckets()
for bucket in response["Buckets"]:
    bucket_name = bucket["Name"]
    print(f"\nBucket: {bucket_name}")

    try:
        policy_response = s3.get_bucket_policy(Bucket=bucket_name)
        policy = json.loads(policy_response["Policy"])
        statements = policy["Statement"]
        
        public_read_found = False

        for statement in statements:
            effect = statement.get("Effect")
            principal = statement.get("Principal")
            action = statement.get("Action")
            # Public read risk: anyone can read objects from the bucket
            if effect == "Allow" and is_public_principal(principal) and has_get_object_action(action):
                public_read_found = True
        if public_read_found:        
            print(f"[HIGH] Bucket {bucket_name} allows public read access")
            high_count += 1
        else:
            print(f"[OK] Bucket {bucket_name} has no public read access")
            ok_count += 1
        
    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "NoSuchBucketPolicy":
            print(f"[OK] Bucket {bucket_name} has no bucket policy")
            ok_count += 1
        else:
            print(f"[ERROR] Failed to check bucket {bucket_name}")
            print(error)
            error_count += 1
print("\nSummary:")
print(f"HIGH findings: {high_count}")
print(f"OK checks: {ok_count}")
print(f"ERROR checks: {error_count}")
        
        