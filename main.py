"""
# TODO !    Hide -> Unhide для скрытых игр
# TODO      Split database into two tables
"""

from Code.Screens.CheckNewGamesOnIGNScreen import CheckNewGamesOnIGNScreen
from Code.Screens.ThisMonthsReleasesScreen import ThisMonthsReleasesScreen
from Code.TeverusSDK.Screen import Screen, SCREEN_WIDTH, Action
from Code.TeverusSDK.Table import Table


class WelcomeScreen(Screen):
    def __init__(self):
        self.actions = [
            Action(name="Check new games on IGN", function=CheckNewGamesOnIGNScreen),
            Action(name="This month's releases", function=ThisMonthsReleasesScreen),
            Action(name="See all releases"),
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
