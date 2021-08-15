import time


class Tracker:

    def __init__(self, cur_index=0) -> None:
        self.active_label = False
        self.cur_index = cur_index
        self.start_time = 0
        self.stop_time = 0

    def start(self) -> float:
        self.start_time = time.time()
        return self.start_time

    def stop(self) -> float:
        self.stop_time = time.time()
        return self.stop_time
