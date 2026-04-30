import os

from google.cloud import compute_v1


def list_instances(project: str | None = None, zone: str | None = None):
    project_id = project or os.getenv("GCP_PROJECT", "project")
    zone_name = zone or os.getenv("GCP_ZONE", "zone")
    client = compute_v1.InstancesClient()
    return list(client.list(project=project_id, zone=zone_name))
