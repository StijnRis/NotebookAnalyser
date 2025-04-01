from datetime import datetime

import numpy as np

from content_log.progression.progression_with_timedelta import ProgressionWithTimedelta


class ProgressionWithDatetime:
    def __init__(self, datetimes: list[datetime], progression: list[float]):
        self.times = [t.timestamp() for t in datetimes]
        self.datetimes = datetimes
        self.data = progression

    def get_progression_at(self, moment: datetime):
        """
        Calculate the progression of a notebook at some time
        """

        if len(self.times) == 0:
            return 0

        return np.interp(
            moment.timestamp(),
            self.times,
            self.data,
            left=self.data[0],
            right=self.data[-1],
        )

    # def get_progression_slope_at(self, moment: datetime):
    #     """
    #     Calculate the speed of progression a notebook at some time.
    #     """

    #     time = moment.timestamp()

    #     return self.notebook_progression.get_gradient_at(time)

    def convert_to_progression_with_timedelta(self):
        return ProgressionWithTimedelta(
            [self.datetimes[i] - self.datetimes[0] for i in range(len(self.datetimes))],
            self.data,
        )

    # TODO little bit weird, but it works
    def combine_through_addition(self, other: "ProgressionWithDatetime"):
        """
        Add two progressions together. It sums the data of the two progressions.
        """
        datetimes = self.datetimes + other.datetimes
        datetimes.sort()

        data = []
        for datetime in datetimes:
            point1 = self.get_progression_at(datetime)
            point2 = other.get_progression_at(datetime)
            total = point1 + point2
            data.append(total)

        return ProgressionWithDatetime(datetimes, data)
