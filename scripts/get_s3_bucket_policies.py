import boto3

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
        print("Policy found:")
        print(policy_response["Policy"])
    except Exception as error:
        print(f"Policy not found for bucket: {bucket_name}")
        print(f"Error: {error}")