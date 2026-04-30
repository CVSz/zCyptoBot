"""Tenant provisioning primitives for isolated AWS workloads."""

from __future__ import annotations

from typing import Any

import boto3

ec2 = boto3.client("ec2")


def create_instance(
    *,
    image_id: str,
    instance_type: str = "t3.medium",
    subnet_id: str | None = None,
    security_group_ids: list[str] | None = None,
    iam_instance_profile: str | None = None,
    tags: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Create an EC2 instance with enterprise defaults."""
    tag_specifications = []
    if tags:
        tag_specifications.append(
            {
                "ResourceType": "instance",
                "Tags": [{"Key": key, "Value": value} for key, value in tags.items()],
            }
        )

    request: dict[str, Any] = {
        "ImageId": image_id,
        "InstanceType": instance_type,
        "MinCount": 1,
        "MaxCount": 1,
        "TagSpecifications": tag_specifications,
    }

    if subnet_id:
        request["SubnetId"] = subnet_id
    if security_group_ids:
        request["SecurityGroupIds"] = security_group_ids
    if iam_instance_profile:
        request["IamInstanceProfile"] = {"Name": iam_instance_profile}

    return ec2.run_instances(**request)
