from datetime import datetime
from pathlib import Path

from Code.Modules.HideGame import HideGame
from Code.Modules.OpenInSteam import OpenInSteam
from Code.Modules.ShowHiddenReleases import ShowHiddenReleases
from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import (
    Screen,
    Action,
    SCREEN_WIDTH,
    GO_BACK,
    do_nothing,
    Key,
)
from Code.TeverusSDK.Table import Table, ColumnWidth


class ThisMonthsReleasesScreen(Screen):
    def __init__(self):
        self.SHOW_HIDDEN = "[S] Show hidden"
        self.EXCLUDE_HIDDEN = "[S] Exclude hidden"

        self.actions = self.get_actions(remove_hidden=True, main=self)

        self.table = self.get_table(self.actions, main=self)

        super(ThisMonthsReleasesScreen, self).__init__(self.table, self.actions)

    ####################################################################################
    #    SCREEN SPECIFIC ACTIONS                                                       #
    ####################################################################################

    @staticmethod
    def get_rows(remove_hidden=False):
        day = datetime.today().strftime("%d").rjust(2, "0")
        month = datetime.today().strftime("%b").upper()
        year = datetime.today().strftime("%Y")
        today = f"{day} {month.capitalize()} {year}"

        db = DataBase(Path("Files/GameReleases.db"))
        df = db.read_table()

        df = df.loc[df.Month == month]
        df = df.loc[df.Hidden == "0"] if remove_hidden else df

        df.reset_index(drop=True, inplace=True)

        games = {}
        for index in range(len(df)):
            game = df.loc[index]
            title = game.Title
            day_ = "?? " if not game.Day else f"{game.Day.rjust(2, '0')} "
            date = f"{day_}{game.Month.capitalize()} {game.Year}"
            games[title] = date

        wall = 3
        side_padding = 2
        hide = 8

        rows = []
        for title, date in games.items():
            mark = ">>> " if date == today else "    "
            mark_and_date = f"{mark}[{date}"
            main_col_width = len(mark_and_date) + (wall * 2) + side_padding + hide
            line = f"{mark_and_date}] {title.ljust(SCREEN_WIDTH - main_col_width)}"
            rows.append(line)

        return rows

    def get_actions(self, remove_hidden, main):
        rows = self.get_rows(remove_hidden=remove_hidden)

        actions = [
            [
                Action(
                    name=row,
                    function=OpenInSteam,
                    arguments={"game_title": row},
                ),
                Action(
                    name="  Hide  ",
                    function=HideGame,
                    arguments={"game_title": row, "main": main},
                ),
            ]
            for row in rows
        ]

        return actions

    def get_table(self, actions, main):
        table = Table(
            table_title=f"This month's releases [{len(actions)}]",
            rows=[[action[0].name, action[1].name] for action in actions],
            table_width=SCREEN_WIDTH,
            max_rows=29,
            highlight=[0, 0],
            column_widths={0: ColumnWidth.FULL, 1: ColumnWidth.FIT},
            footer=[
                Action(
                    name=GO_BACK,
                    function=do_nothing,
                    go_back=True,
                    shortcut=[Key.Q, Key.Q_RU],
                ),
                Action(
                    name=self.SHOW_HIDDEN,
                    function=ShowHiddenReleases,
                    arguments={"main": main},
                    shortcut=[Key.S, Key.S_RU],
                ),
            ],
        )

        return table
