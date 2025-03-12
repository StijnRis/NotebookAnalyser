import numpy as np


class TimeSeries:
    def __init__(self, times: list[float], data: list[float]):
        self.times = times
        self.data = data
