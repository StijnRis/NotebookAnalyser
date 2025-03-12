from datetime import datetime

from notebook_log.progression.notebook_progression import NotebookProgression


class NotebookProgressionWithDatetime:
    def __init__(self, datetimes: list[datetime], progression: list[float]):
        self.times = [t.timestamp() for t in datetimes]
        self.datetimes = datetimes
        self.data = progression
        self.notebook_progression = NotebookProgression(self.times, self.data)

    def get_progression_at(self, moment: datetime):
        """
        Calculate the progression of a notebook at some time
        """

        time = moment.timestamp()

        return self.notebook_progression.get_progression_at(time)

    def get_progression_slope_at(self, moment: datetime):
        """
        Calculate the speed of progression a notebook at some time.
        """

        time = moment.timestamp()

        return self.notebook_progression.get_gradient_at(time)

    def convert_to_notebook_progression(self):
        return self.notebook_progression
