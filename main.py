from Code.Screens.old.z_CheckNewGamesOnIGNScreen import CheckNewGamesOnIGNScreen
from Code.Screens.ThisMonthsReleasesScreen import ThisMonthsReleasesScreen
from Code.TeverusSDK.old.z_Screen import Screen, Action, SCREEN_WIDTH
from Code.TeverusSDK.old.z_Table import Table
from Code.TeverusSDK.TableV2 import TableV2


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
            footer_bottom_border=False,
        )

        self.table2 = TableV2(
            table_title="Game releases tracker",
            rows=[action.name for action in self.actions],
            rows_bottom_border=False,
            footer_bottom_border=False,
            table_width=SCREEN_WIDTH,
        )

        super(WelcomeScreen, self).__init__(self.table, self.actions)


if __name__ == "__main__":
    WelcomeScreen()
