from Code.Screens.CheckNewGamesOnIGN import CheckNewGamesOnIGN
from Code.TeverusSDK.Screen import Screen, Action
from Code.TeverusSDK.Table import Table


class WelcomeScreen(Screen):
    def __init__(self):
        actions = [
            Action(name="Check new games on IGN", function=CheckNewGamesOnIGN),
            Action(name="This month's releases"),
            Action(name="Future releases"),
            Action(name="Releases by game genre"),
        ]

        table = Table(
            table_title="Game releases tracker",
            rows=[action.name for action in actions],
            table_width=100,
        )

        super(WelcomeScreen, self).__init__(table, actions)


if __name__ == "__main__":
    WelcomeScreen()
