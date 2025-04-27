from analyser.analyser import Analyser
from report.column.text_column import TextColumn
from user.user import User


class FileActivityAnalyser(Analyser):
    """
    Generate report of users file activities
    """

    def __init__(self):
        super().__init__()
        self.sheet.add_columns(
            [
                TextColumn("Username"),
                TextColumn("Used ai codes"),
                TextColumn("Similarities with AI"),
            ]
        )

    def analyse_user(self, user: User):
        username = user.get_username()
        file_activities = user.get_file_activities()

        for file_activity in file_activities:
            self.sheet.add_row(
                {
                    "Username": username,
                    "Used ai codes": ",".join(file_activity.get_used_ai_code()),
                    "Similarities with AI": ",".join(
                        str(
                            file_activity.get_similarities_between_ai_code_and_cell(
                                file_activity.get_file_log().get_end_active_time()
                            )
                        )
                    ),
                }
            )
