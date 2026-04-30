def map_to_sa(claims):
    return {"serviceAccount": f"{claims['tenant']}@project.iam.gserviceaccount.com"}
