from datetime import timedelta


class TimedeltaSeries:
    def __init__(self, data: list[tuple[timedelta, float]]):
        self.data = data

    def get_data(self) -> list[tuple[timedelta, float]]:
        return self.data

    def convert_to_list_of_tuples(self) -> list[tuple[float, float]]:
        return [(x[0].total_seconds(), x[1]) for x in self.data]
