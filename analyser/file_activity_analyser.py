from analyser.analyser import Analyser
from user.user import User


class FileActivityAnalyser(Analyser):
    """
    Generate report of user notebook
    """

    def __init__(self):
        super().__init__()

    def analyse_user(self, user: User):
        username = user.get_username()
        file_activities = user.get_file_activities()

        for file_activity in file_activities:
            user_data = {
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

            self.data.append(user_data)
