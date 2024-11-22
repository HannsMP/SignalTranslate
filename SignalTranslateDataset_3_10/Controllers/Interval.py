from time import time, sleep


class Inteval:
    def __init__(self, err: bool = False):
        self.err = 0.0

        if (err):
            e1 = 0.0001
            self.start()
            sleep(e1)
            e2 = self.end()
            self.err = e2 - e1

    def _reset_(self):
        self.start_time = 0
        self.prom = 0
        self.min = float('inf')
        self.max = float('-inf')

    def start(self):
        self._reset_()
        self.start_time = time()

    def end(self):
        res = time() - self.start_time
        self.prom = round((self.prom + res) / 2, 3)
        self.min = round(min(self.min, res), 3)
        self.max = round(max(self.max, res), 3)
        return round(res - self.err, 3)


if __name__ == "__main__":
    interval = Inteval(True)

    interval.start()

    sleep(1)

    print(interval.end())
