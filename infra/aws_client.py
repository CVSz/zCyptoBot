import os

import boto3


def list_instances(region: str | None = None):
    ec2 = boto3.client("ec2", region_name=region or os.getenv("AWS_REGION", "us-east-1"))
    return ec2.describe_instances()
