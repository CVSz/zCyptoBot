import json
import time


def log(event):
    print(json.dumps({"ts": time.time(), **event}))
