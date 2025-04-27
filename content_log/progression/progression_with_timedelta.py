from datetime import datetime, timedelta


class ProgressionWithTimedelta:
    def __init__(self, times: list[timedelta], progression: list[float]):
        assert len(times) == len(
            progression
        ), "Times and progression must be the same length"
        self.times = times
        self.progression = progression

    def get_times(self) -> list[timedelta]:
        return self.times

    def get_progression(self) -> list[float]:
        return self.progression

    def convert_to_list_of_tuples(self) -> list[tuple[float, float]]:
        return list(zip([x.total_seconds() for x in self.times], self.progression))
