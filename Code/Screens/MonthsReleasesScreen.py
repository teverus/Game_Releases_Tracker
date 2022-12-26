import re
from datetime import datetime
from pathlib import Path

from Code.Modules.ChangeGameStatus import ChangeGameStatus
from Code.Modules.OpenInSteam import OpenInSteam
from Code.Modules.ShowHiddenReleases import ShowHiddenReleases
from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import (
    Screen,
    Action,
    SCREEN_WIDTH,
    Key,
    GO_BACK_ACTION,
)
from Code.TeverusSDK.Table import Table, ColumnWidth


class MonthsReleasesScreen(Screen):
    def __init__(self, **kwargs):
        date = kwargs["month_and_year"]
        self.month_and_year = datetime.strptime(date, "%B %Y").strftime("%b %Y")
        self.SHOW_HIDDEN = "[S] Show hidden"
        self.EXCLUDE_HIDDEN = "[S] Exclude hidden"
        self.database = DataBase(Path("Files/GameReleases.db"))

        self.actions = self.get_actions(remove_hidden=True, main=self)

        self.table = self.get_table(self.actions, main=self)

        super(MonthsReleasesScreen, self).__init__(self.table, self.actions)

    ####################################################################################
    #    PRIMARY ACTIONS                                                               #
    ####################################################################################

    def get_actions(self, remove_hidden, main):
        rows = self.get_rows(main, remove_hidden)

        actions = []
        for game, hidden in rows.items():
            game_title = re.findall(r"\[.*\w{3}.\d{4}\].(.*)", game)[0].strip()

            main_action = Action(
                name=game,
                function=OpenInSteam,
                arguments={"game_title": game_title},
            )

            secondary_action = Action(
                name="  Hide  " if not hidden else " Unhide ",
                function=ChangeGameStatus,
                arguments={"game_title": game_title, "main": main},
            )

            actions.append([main_action, secondary_action])

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
                GO_BACK_ACTION,
                Action(
                    name=self.SHOW_HIDDEN,
                    function=ShowHiddenReleases,
                    arguments={"main": main},
                    shortcut=[Key.S, Key.S_RU],
                ),
            ],
        )

        return table

    ####################################################################################
    #    HELPERS                                                                       #
    ####################################################################################
    def get_rows(self, main, remove_hidden=False):
        day = datetime.today().strftime("%d").rjust(2, "0")
        month = datetime.today().strftime("%b").upper()
        year = datetime.today().strftime("%Y")
        today = f"{day} {month.capitalize()} {year}"

        df = self.database.read_table()

        df = df.loc[df.MonthAndYear == f"{main.month_and_year.upper()}"]
        df = df.loc[df.Hidden == "0"] if remove_hidden else df

        df.reset_index(drop=True, inplace=True)

        wall = 3
        side_padding = 2
        hide = 8

        games = {}
        for index in range(len(df)):
            game = df.loc[index]
            title = game.Title
            hidden = bool(int(game.Hidden))
            day_ = "??" if not game.Day else f"{game.Day.rjust(2, '0')}"
            date = f"{day_} {game.MonthAndYear.title()}"

            mark = ">>> " if date == today else "    "
            mark_and_date = f"{mark}[{date}"
            main_col_width = len(mark_and_date) + (wall * 2) + side_padding + hide
            line = f"{mark_and_date}] {title.ljust(SCREEN_WIDTH - main_col_width)}"
            games[line] = hidden

        return games
