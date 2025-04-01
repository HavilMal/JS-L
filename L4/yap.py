import sys
import time

def run():
    while True:
        time.sleep(0.5)
        try:
            sys.stdout.write("yap\n")
            sys.stdout.flush()
        except Exception:
            return


run()