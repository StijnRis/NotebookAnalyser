from datetime import timedelta


class ProgressionWithTimedelta:
    def __init__(self, times: list[timedelta], progression: list[float]):
        self.times = times
        self.progression = progression

    def get_times(self) -> list[timedelta]:
        return self.times

    def get_progression(self) -> list[float]:
        return self.progression

    def remove_idle_time(self, idle_threshold: timedelta):
        """
        Calculate the progression of file content over working time.
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

    def convert_to_list_of_tuples(self) -> list[tuple[float, float]]:
        return list(zip([x.total_seconds() for x in self.times], self.progression))
