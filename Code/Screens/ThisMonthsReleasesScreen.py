from pathlib import Path

from Code.Modules.HideGame import HideGame
from Code.Modules.OpenInSteam import OpenInSteam
from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import Screen, SCREEN_WIDTH, Action, do_nothing, GO_BACK
from Code.TeverusSDK.Table import Table, ColumnWidth

from datetime import datetime


class ThisMonthsReleasesScreen(Screen):
    def __init__(self):

        day = datetime.today().strftime("%d").rjust(2, "0")
        month = datetime.today().strftime("%b").upper()
        year = datetime.today().strftime("%Y")
        today = f"{day} {month.capitalize()} {year}"

        self.db = DataBase(Path("Files/GameReleases.db"))
        self.df = self.db.read_table()
        self.df = self.df.loc[(self.df.Month == month) & (self.df.Hidden != "1")]
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
            for row in rows
        ]

        self.table = Table(
            table_title="This month's releases",
            table_width=SCREEN_WIDTH,
            rows=[[a[0].name, a[1].name] for a in self.actions],
            max_rows=29,
            column_widths={0: ColumnWidth.FIT, 1: ColumnWidth.FULL},
            footer_actions=[
                Action(name=GO_BACK, function=do_nothing, go_back=True),
                # TODO Реализовать вот это
                Action(name="[S] Show hidden", function=do_nothing),
            ],
            footer_bottom_border="",
        )

        super(ThisMonthsReleasesScreen, self).__init__(self.table, self.actions)
