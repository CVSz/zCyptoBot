import requests


def test(url: str, token: str) -> int:
    r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=3)
    return r.status_code


if __name__ == "__main__":
    print(test("http://gateway/app", "gid-token"))
