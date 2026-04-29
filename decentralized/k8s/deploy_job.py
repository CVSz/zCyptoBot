from kubernetes import client, config


def deploy(node_id: str, job_id: str, qty: float):
    # assumes kubeconfig present
    config.load_kube_config()
    api = client.BatchV1Api()

    job = client.V1Job(
        metadata=client.V1ObjectMeta(name=f"job-{job_id}"),
        spec=client.V1JobSpec(
            template=client.V1PodTemplateSpec(
                spec=client.V1PodSpec(
                    restart_policy="Never",
                    containers=[
                        client.V1Container(
                            name="worker",
                            image="busybox",
                            command=["sh", "-c", f"echo running {job_id}; sleep {int(5 + qty)}"],
                        )
                    ],
                    # optionally add nodeSelector/affinity per node_id mapping
                )
            )
        ),
    )
    api.create_namespaced_job(namespace="default", body=job)
