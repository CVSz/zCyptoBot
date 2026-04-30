import time
LOG = []
def log(event):
    LOG.append({**event, "ts": time.time()})
