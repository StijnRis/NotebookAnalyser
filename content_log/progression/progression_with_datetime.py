from datetime import datetime, timedelta

import numpy as np

from content_log.progression.progression_with_timedelta import ProgressionWithTimedelta


class ProgressionWithDatetime:
    def __init__(self, datetimes: list[datetime], progression: list[float]):
        assert len(datetimes) == len(
            progression
        ), "Datetimes and progression must be the same length"
        self.times = [t.timestamp() for t in datetimes]
        self.datetimes = datetimes
        self.data = progression

    def get_progression_at(self, moment: datetime):
        """
        Calculate the progression of a file at some time
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

    def convert_to_progression_with_timedelta(self):
        return ProgressionWithTimedelta(
            [self.datetimes[i] - self.datetimes[0] for i in range(len(self.datetimes))],
            self.data,
        )

    def select_periods(
        self, active_time: list[tuple[datetime, datetime]]
    ) -> ProgressionWithTimedelta:
        """
        Select the active time of the progression. It returns a new ProgressionWithTimedelta object.
        """

        selected_times: list[timedelta] = []
        selected_progression: list[float] = []
        offset = timedelta(0)

        active_time_index = 0
        for i, time in enumerate(self.datetimes):
            while (
                active_time_index < len(active_time)
                and time > active_time[active_time_index][1]
            ):
                offset += (
                    active_time[active_time_index][1]
                    - active_time[active_time_index][0]
                )
                active_time_index += 1

            if (
                active_time_index < len(active_time)
                and active_time[active_time_index][0]
                <= time
                <= active_time[active_time_index][1]
            ):
                selected_times.append(time - active_time[active_time_index][0] + offset)
                selected_progression.append(self.data[i])
            else:
                print(time.timestamp())
                raise ValueError(
                    f"Time {time} is not in the active time range {active_time[active_time_index][0]} - {active_time[active_time_index][1]}"
                )

        return ProgressionWithTimedelta(selected_times, selected_progression)

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
