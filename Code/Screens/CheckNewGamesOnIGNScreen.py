from Code.Modules.UpdateGames import UpdateGames
from Code.TeverusSDK.Screen import Screen, Action, SCREEN_WIDTH
from Code.TeverusSDK.Table import Table


class CheckNewGamesOnIGNScreen(Screen):
    def __init__(self):
        actions = [
            Action(
                name=" ",
                function=UpdateGames,
                immediate_action=True,
                go_back=True,
            )
        ]

        table = Table(
            table_title="Check new games on IGN",
            rows=[action.name for action in actions],
            highlight=False,
            rows_bottom_border="",
            table_width=SCREEN_WIDTH,
        )

        super(CheckNewGamesOnIGNScreen, self).__init__(table, actions)
