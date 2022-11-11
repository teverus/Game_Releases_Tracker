from Code.Screens.CheckNewGamesOnIGNScreen import CheckNewGamesOnIGNScreen
from Code.Screens.ThisMonthsReleasesScreen import ThisMonthsReleasesScreen
from Code.TeverusSDK.ScreenV2 import ScreenV2, SCREEN_WIDTH, Action
from Code.TeverusSDK.TableV2 import TableV2


class WelcomeScreenV2(ScreenV2):
    def __init__(self):
        self.actions = [
            Action(name="Check new games on IGN", function=CheckNewGamesOnIGNScreen),
            Action(name="This month's releases", function=ThisMonthsReleasesScreen),
            Action(name="See all releases"),
            Action(name="Releases by game genre"),
        ]

        self.table = TableV2(
            table_title="Game releases tracker",
            rows=[a.name for a in self.actions],
            rows_bottom_border=False,
            table_width=SCREEN_WIDTH,
        )

        super(WelcomeScreenV2, self).__init__(self.table, self.actions)


if __name__ == "__main__":
    WelcomeScreenV2()
