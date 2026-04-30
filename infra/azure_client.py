import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient


def list_instances(subscription_id: str | None = None):
    resolved_subscription = subscription_id or os.getenv("AZURE_SUBSCRIPTION_ID", "subscription_id")
    client = ComputeManagementClient(DefaultAzureCredential(), resolved_subscription)
    return client.virtual_machines.list_all()
