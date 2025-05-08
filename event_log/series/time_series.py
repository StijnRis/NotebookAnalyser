from datetime import datetime, timedelta

import numpy as np

from event_log.series.timedelta_series import TimedeltaSeries


class TimeSeries:
    def __init__(self, data: list[tuple[datetime, float]]):
        self.data = data
        self.times = [t[0].timestamp() for t in self.data]
        self.datetimes = [t[0] for t in self.data]
        self.items = [t[1] for t in self.data]

    def get_progression_at(self, moment: datetime):
        """
        Calculate the progression of a file at some time
        """

        if len(self.times) == 0:
            return 0

        return np.interp(
            moment.timestamp(),
            self.times,
            self.items,
            left=self.items[0],
            right=self.items[-1],
        )

    def combine_through_interpolation(self, other: "TimeSeries"):
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
            data.append((datetime, total))

        return TimeSeries(data)

    def combine_through_concattenation(self, other: "TimeSeries"):
        """
        Add two progressions together. It sums the data of the two progressions.
        """
        data = self.data + other.data
        data.sort(key=lambda x: x[0])

        return TimeSeries(data)

    def convert_to_progression_with_timedelta(self):
        return TimedeltaSeries(
            [
                (self.data[i][0] - self.data[0][0], self.data[i][1])
                for i in range(len(self.data))
            ],
        )

    def select_periods(
        self, active_time: list[tuple[datetime, datetime]], start_value, end_value
    ) -> TimedeltaSeries:
        """
        Select the active time of the progression. It returns a new ProgressionWithTimedelta object.
        """

        if len(self.data) == 0:
            return TimedeltaSeries([])

        selected_data: list[tuple[timedelta, float]] = [(timedelta(0), start_value)]

        offset = timedelta(0)
        active_time_index = 0
        for i, item in enumerate(self.data):
            time = item[0]
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
                selected_data.append(
                    (time - active_time[active_time_index][0] + offset, item[1])
                )
            else:
                raise ValueError(
                    f"Time {time} is not in the active time range {active_time[active_time_index][0]} - {active_time[active_time_index][1]}"
                )

        while active_time_index < len(active_time):
            offset += (
                active_time[active_time_index][1] - active_time[active_time_index][0]
            )
            active_time_index += 1

        selected_data.append((offset, end_value))

        return TimedeltaSeries(selected_data)
