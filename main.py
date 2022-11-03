from Code.Screens.CheckNewGamesOnIGNScreen import CheckNewGamesOnIGNScreen
from Code.Screens.ThisMonthsReleasesScreen import ThisMonthsReleasesScreen
from Code.TeverusSDK.Screen import Screen, Action, do_nothing, SCREEN_WIDTH
from Code.TeverusSDK.Table import Table


# TODO Если на главной нажать X, то больше нельзя переключиться :(


class WelcomeScreen(Screen):
    def __init__(self):
        actions = [
            Action(name="Check new games on IGN", function=CheckNewGamesOnIGNScreen),
            Action(name="This month's releases", function=ThisMonthsReleasesScreen),
            Action(name="Future releases"),
            Action(name="Releases by game genre"),
        ]

        table = Table(
            table_title="Game releases tracker",
            rows=[action.name for action in actions],
            table_width=SCREEN_WIDTH,
            footer_actions=[Action(name="[Q] Exit", function=do_nothing, go_back=True)],
            footer_bottom_border="",
        )

        super(WelcomeScreen, self).__init__(table, actions)


if __name__ == "__main__":
    WelcomeScreen()
