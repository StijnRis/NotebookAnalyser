from datetime import datetime
from re import S

import numpy as np

from common.time_series import TimeSeries


class NotebookProgression(TimeSeries):
    def __init__(self, times, progression):
        super().__init__(times, progression)
        self.idle_threshold_seconds = 3600

    def get_progression_at(self, time: datetime):
        """
        Calculate the progression of a notebook at some time
        """

        times_seconds = [(t - self.times[0]).total_seconds() for t in self.times]
        time_seconds = (time - self.times[0]).total_seconds()

        return np.interp(
            time_seconds,
            times_seconds,
            self.data,
            self.data[0],
            self.data[-1],
        )
    
    def get_progression_slope_at(self, time: datetime):
        """
        Calculate the speed of progression a notebook at some time.
        """

        times_seconds = [(t - self.times[0]).total_seconds() for t in self.times]
        time_seconds = (time - self.times[0]).total_seconds()

        gradients = np.gradient(self.data)
        return np.interp(
            time_seconds,
            times_seconds,
            gradients,
            self.data[0],
            self.data[-1],
        )
    
    def get_progression_over_working_time(self):
        """
        Calculate the progression of notebook content over working time.
        """

        working_times: list[float] = []
        last_time = None
        working_time: float = 0.0

        for time in self.times:
            if last_time is not None:
                time_diff = (time - last_time).total_seconds()
                if time_diff < self.idle_threshold_seconds:
                    working_time += time_diff
            working_times.append(working_time)
            last_time = time

        return NotebookProgression(working_times, self.data)

    def get_gradient(self):
        """
        Calculate the gradient of the progression
        """

        gradient_values = np.gradient(self.data)
        return TimeSeries(self.times, gradient_values)