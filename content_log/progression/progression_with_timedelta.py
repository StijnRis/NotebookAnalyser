from datetime import timedelta

from content_log.progression.progression import Progression
from content_log.progression.time_series import TimeSeries


class ProgressionWithTimedelta(Progression):
    def __init__(self, times: list[timedelta], progression: list[float]):
        self.times = times
        self.progression = progression

    def get_times(self) -> list[float]:
        return [t.total_seconds() for t in self.times]

    def get_progression(self) -> list[float]:
        return self.progression

    # def get_gradient(self):
    #     """
    #     Calculate the derivative of the progression
    #     """

    #     gradient = np.diff(self.data) / np.diff(self.times)

    #     if len(gradient) == 0:
    #         return TimeSeries([], [])

    #     # Create the extended time and gradient using NumPy operations
    #     extended_time = (
    #         np.hstack([self.times[:-1], self.times[1:]]).reshape(2, -1).T.flatten()
    #     )
    #     extended_gradient = np.repeat(gradient, 2)

    #     # Append the last time point and gradient
    #     extended_time = np.append(extended_time, self.times[-1])
    #     extended_gradient = np.append(extended_gradient, extended_gradient[-1])

    #     return TimeSeries(extended_time.tolist(), extended_gradient.tolist())

    # def get_gradient_at(self, moment: float):
    #     """
    #     Calculate the speed of progression a notebook at a moment.
    #     """

    #     gradient = np.diff(self.data) / np.diff(self.times)

    #     idx = np.searchsorted(self.times, moment, side="right")
    #     if idx == 0:
    #         return 0
    #     elif idx >= len(gradient):
    #         return 0
    #     else:
    #         return gradient[idx - 1]

    def remove_idle_time(self, idle_threshold: timedelta):
        """
        Calculate the progression of notebook content over working time.
        """

        working_times: list[timedelta] = []
        last_time = None
        working_time: timedelta = timedelta(0)

        for time in self.times:
            if last_time is not None:
                time_diff = time - last_time
                if time_diff < idle_threshold:
                    working_time += time_diff
            working_times.append(working_time)
            last_time = time

        return ProgressionWithTimedelta(working_times, self.progression)

    def convert_to_time_series(self):
        return TimeSeries(self.get_times(), self.progression)
