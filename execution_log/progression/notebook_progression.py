import numpy as np

from content_log.progression.time_series import TimeSeries


class NotebookProgression(TimeSeries):
    def __init__(self, times: list[float], progression: list[float]):
        super().__init__(times, progression)
    
    def get_progression_at(self, moment: float):
        """
        Calculate the progression of a notebook at a moment
        """

        return np.interp(
            moment,
            self.times,
            self.data,
            left=self.data[0],
            right=self.data[-1],
        )

    def get_gradient(self):
        """
        Calculate the derivative of the progression
        """

        gradient = np.diff(self.data) / np.diff(self.times)

        if len(gradient) == 0:
            return TimeSeries([], [])

        # Create the extended time and gradient using NumPy operations
        extended_time = (
            np.hstack([self.times[:-1], self.times[1:]]).reshape(2, -1).T.flatten()
        )
        extended_gradient = np.repeat(gradient, 2)

        # Append the last time point and gradient
        extended_time = np.append(extended_time, self.times[-1])
        extended_gradient = np.append(extended_gradient, extended_gradient[-1])

        return TimeSeries(extended_time.tolist(), extended_gradient.tolist())

    def get_gradient_at(self, moment: float):
        """
        Calculate the speed of progression a notebook at a moment.
        """

        gradient = np.diff(self.data) / np.diff(self.times)

        idx = np.searchsorted(self.times, moment, side='right')
        if idx == 0:
            return 0
        elif idx >= len(gradient):
            return 0
        else:
            return gradient[idx - 1]

    def remove_idle_time(self, idle_threshold_seconds: float = 3600):
        """
        Calculate the progression of notebook content over working time.
        """

        working_times: list[float] = []
        last_time = None
        working_time: float = 0.0

        for time in self.times:
            if last_time is not None:
                time_diff = time - last_time
                if time_diff < idle_threshold_seconds:
                    working_time += time_diff
            working_times.append(working_time)
            last_time = time

        return NotebookProgression(working_times, self.data)
