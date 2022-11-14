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

        self.db = None
        self.df = None
        self.rows = self.get_rows(remove_hidden=True)

        self.actions = [
            [
                Action(
                    name=row,
                    function=OpenInSteam,
                    arguments={"game_title": row},
                ),
                Action(
                    name="Hide",
                    function=HideGame,
                    arguments={"game_title": row, "main": self},
                ),
            ]
            for row in self.rows
        ]

        self.table = Table(
            table_title="This month's releases",
            rows=[[action[0].name, action[1].name] for action in self.actions],
            table_width=SCREEN_WIDTH,
            max_rows=29,
            column_widths={0: ColumnWidth.FIT, 1: ColumnWidth.FULL},
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
                    arguments={"main": self},
                    shortcut=[Key.S, Key.S_RU],
                ),
            ],
        )

        super(ThisMonthsReleasesScreen, self).__init__(self.table, self.actions)

    ####################################################################################
    #    SCREEN SPECIFIC ACTIONS                                                       #
    ####################################################################################

    def get_rows(self, remove_hidden=False):
        day = datetime.today().strftime("%d").rjust(2, "0")
        month = datetime.today().strftime("%b").upper()
        year = datetime.today().strftime("%Y")
        today = f"{day} {month.capitalize()} {year}"

        self.db = DataBase(Path("Files/GameReleases.db"))
        self.df = self.db.read_table()

        self.df = self.df.loc[self.df.Month == month]
        self.df = self.df.loc[self.df.Hidden == "0"] if remove_hidden else self.df

        self.df.reset_index(drop=True, inplace=True)

        games = {}
        for index in range(len(self.df)):
            game = self.df.loc[index]
            title = game.Title
            day_ = "?? " if not game.Day else f"{game.Day.rjust(2, '0')} "
            date = f"{day_}{game.Month.capitalize()} {game.Year}"
            games[title] = date

        max_len = max([len(title) for title in games.keys()])
        rows = []
        for title, date in games.items():
            mark = ">>> " if date == today else "    "
            line = f"{mark}{date} | {title.ljust(max_len)}"
            rows.append(line)

        return rows
