from Code.Modules.UpdateGames import UpdateGames
from Code.TeverusSDK.ScreenV2 import ScreenV2, Action, SCREEN_WIDTH
from Code.TeverusSDK.TableV2 import TableV2


class CheckNewGamesOnIGNScreen(ScreenV2):
    def __init__(self):
        self.actions = [
            Action(
                name=" ",
                function=UpdateGames,
                immediate_action=True,
                go_back=True,
            )
        ]

        self.table = TableV2(
            table_title="Check new games on IGN",
            rows=[action.name for action in self.actions],
            highlight=False,
            rows_bottom_border=False,
            table_width=SCREEN_WIDTH,
        )

        super(CheckNewGamesOnIGNScreen, self).__init__(self.table, self.actions)
