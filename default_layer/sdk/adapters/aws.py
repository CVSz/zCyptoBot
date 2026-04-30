def map_to_iam(claims):
    return {"role": f"arn:aws:iam::{claims['tenant']}:role/app"}
