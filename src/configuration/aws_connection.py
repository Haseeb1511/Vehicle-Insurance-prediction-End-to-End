import boto3
import os
from src.constant import AWS_ACCESS_KEY_ID_ENV_KEY,AWS_SECRET_ACCESS_KEY_ENV_KEY,REGION_NAME
from dotenv import load_dotenv
load_dotenv()

class S3Client:
    s3_client = None
    s3_resource = None

    def __init__(self,region_name=REGION_NAME):
        if S3Client.s3_client ==None or S3Client.s3_resource==None:
            __access_key_id = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
            __secret_access_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)
            if __access_key_id is None:
                raise Exception(f"Enviroment variable is not set{AWS_ACCESS_KEY_ID_ENV_KEY}")
            if __secret_access_key is None:
                raise Exception(f"Enviroment variable is not set{AWS_SECRET_ACCESS_KEY_ENV_KEY}")
            
            S3Client.s3_resource = boto3.resource('s3',
                                            aws_access_key_id=__access_key_id,
                                            aws_secret_access_key=__secret_access_key,
                                            region_name=region_name
                                            )
            S3Client.s3_client = boto3.client('s3',
                                        aws_access_key_id=__access_key_id,
                                        aws_secret_access_key=__secret_access_key,
                                        region_name=region_name
                                        )
        self.s3_resource = S3Client.s3_resource
        self.s3_client = S3Client.s3_client



# boto3.client('s3')
# This is a low-level service client.
# It maps directly to AWS API calls (one-to-one).
# You control the exact requests and responses.
# Example: s3_client.list_buckets()


# boto3.resource('s3')
# This is a high-level object-oriented resource.
# It provides classes like Bucket, Object, etc.
# It lets you interact with AWS in a more Pythonic way.
# Example: s3_resource.Bucket('my-bucket').put_object(Key='key', Body=b'data')

#  Both do the same thing, but the resource version feels more object-oriented.
# If you like low-level, explicit control → use client only.
# If you want high-level, cleaner code → use resource.