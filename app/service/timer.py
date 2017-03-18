import time


class Timer:
    def __init__(self):
        self.start = time.time()

    def stop(self):
        print(time.time() - self.start)

    def allo(self):
        self.start = time.time()


TIMER = Timer()
