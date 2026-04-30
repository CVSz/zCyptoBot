import time


def loop(fn, interval=60):
    while True:
        fn()
        time.sleep(interval)
