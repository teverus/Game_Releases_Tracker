from pathlib import Path

from Code.Modules.OpenGameInSteam import OpenGameInSteam
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

        df = DataBase(Path("Files/GameReleases.db")).read_table()
        df = df.loc[df.Month == month]
        df.reset_index(drop=True, inplace=True)

        games = {}
        for index in range(len(df)):
            game = df.loc[index]
            title = game.Title
            day_ = "?? " if not game.Day else f"{game.Day.rjust(2, '0')} "
            date = f"{day_}{game.Month.capitalize()} {game.Year}"
            games[title] = date

        max_len = max([len(title) for title in games.keys()])
        rows = []
        for title, date in games.items():
            mark = ">>> " if date == today else "    "
            line = f"{mark}{date} | {title.ljust(max_len)}".center(SCREEN_WIDTH - 2)
            rows.append(line)

        actions = [
            Action(name=row, function=OpenGameInSteam, arguments={"game_title": row})
            for row in rows
        ]

        table = Table(
            table_title="This month's releases",
            table_width=SCREEN_WIDTH,
            rows=[action.name for action in actions],
            max_rows=30,
            column_widths={0: ColumnWidth.FIT, 1: ColumnWidth.FULL},
            footer_actions=[Action(name=GO_BACK, function=do_nothing, go_back=True)],
            footer_bottom_border="",
        )

        super(ThisMonthsReleasesScreen, self).__init__(table, actions)
