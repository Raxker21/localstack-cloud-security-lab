import boto3

s3 = boto3.client("s3",
                endpoint_url="http://localhost.localstack.cloud:4566",
                aws_access_key_id="test",
                aws_secret_access_key="test",
                region_name="us-east-1",
                )

response = s3.list_buckets() #Запрашивает у S3 список всех bucket
for bucket in response["Buckets"]: #берет bucket из списка ["Bucket"] в response
    print (bucket["Name"]) 