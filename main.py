from datetime import datetime

from Code.Screens.AllRecordedReleasesScreen import AllRecordedReleasesScreen
from Code.Screens.CheckNewGamesOnIGNScreen import CheckNewGamesOnIGNScreen
from Code.Screens.MonthsReleasesScreen import MonthsReleasesScreen
from Code.TeverusSDK.Screen import Screen, SCREEN_WIDTH, Action
from Code.TeverusSDK.Table import Table


class WelcomeScreen(Screen):
    def __init__(self):
        self.actions = [
            Action(
                name="Check new games on IGN",
                function=CheckNewGamesOnIGNScreen,
            ),
            Action(
                name="This month's releases",
                function=MonthsReleasesScreen,
                arguments={"month_and_year": datetime.today().strftime("%B %Y")},
            ),
            Action(
                name="All recorded releases",
                function=AllRecordedReleasesScreen,
            ),
            Action(name="Releases by game genre"),
        ]

        self.table = Table(
            table_title="Game releases tracker",
            rows=[action.name for action in self.actions],
            rows_bottom_border=False,
            table_width=SCREEN_WIDTH,
        )

        super(WelcomeScreen, self).__init__(self.table, self.actions)


if __name__ == "__main__":
    WelcomeScreen()
