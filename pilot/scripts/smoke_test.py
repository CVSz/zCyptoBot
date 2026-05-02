import os
import argparse
import requests


def test(url: str, token: str) -> int:
    r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=3)
    return r.status_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=os.getenv("SMOKE_TEST_URL", "http://gateway/app"))
    parser.add_argument("--token", default=os.getenv("SMOKE_TEST_TOKEN"))
    args = parser.parse_args()

    if not args.token:
        print("SMOKE_TEST_TOKEN not set; aborting")
        raise SystemExit(1)

    print(test(args.url, args.token))
