import re
from datetime import datetime
from pathlib import Path

from Code.Modules.ChangeVisibilityStatus import ChangeVisibilityStatus, HIDE, UNHIDE
from Code.Modules.OpenInSteam import OpenInSteam
from Code.Modules.ChangePinStatus import ChangePinStatus, PIN, UNPIN
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
        for game, statuses in rows.items():
            hidden, pinned = statuses
            game_title = re.findall(r"\[.*\w{3}.\d{4}\].(.*)", game)[0].strip()

            main_action = Action(
                name=game,
                function=OpenInSteam,
                arguments={"game_title": game_title},
            )

            secondary_action = Action(
                name=HIDE if not hidden else UNHIDE,
                function=ChangeVisibilityStatus,
                arguments={"game_title": game_title, "main": main},
            )

            tertiary_action = Action(
                name=PIN if not pinned else UNPIN,
                function=ChangePinStatus,
                arguments={"game_title": game_title, "main": main},
            )

            actions.append([main_action, secondary_action, tertiary_action])

        return actions

    def get_table(self, actions, main):
        table = Table(
            table_title=f"This month's releases [{len(actions)}]",
            rows=[[a[0].name, a[1].name, a[2].name] for a in actions],
            table_width=SCREEN_WIDTH,
            max_rows=29,
            highlight=[0, 0],
            column_widths={0: ColumnWidth.FIT, 1: ColumnWidth.FIT, 2: ColumnWidth.FIT},
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
        today = self.get_today()
        df = self.get_df(main, remove_hidden)

        wall = 2
        side_padding = 2
        hide = 8
        pin = 7

        games = {}
        for index in range(len(df)):
            game = df.loc[index]
            title = game.Title
            hidden = bool(int(game.Hidden))
            pinned = bool(int(game.Pinned))
            day_ = "??" if not game.Day else f"{game.Day.rjust(2, '0')}"
            date = f"{day_} {game.MonthAndYear.title()}"

            mark = "### " if pinned else "    "
            mark = ">>> " if date == today else mark
            mark_and_date = f"{mark}[{date}"
            main_col_width = len(mark_and_date) + (wall * 2) + side_padding + hide + pin
            line = f"{mark_and_date}] {title.ljust(SCREEN_WIDTH - main_col_width)}"
            games[line] = [hidden, pinned]

        return games

    @staticmethod
    def get_today():
        day = datetime.today().strftime("%d").rjust(2, "0")
        month = datetime.today().strftime("%b").upper()
        year = datetime.today().strftime("%Y")
        today = f"{day} {month.capitalize()} {year}"

        return today

    def get_df(self, main, remove_hidden):
        df = self.database.read_table()

        df = df.loc[df.MonthAndYear == f"{main.month_and_year.upper()}"]
        df = df.loc[df.Hidden == "0"] if remove_hidden else df

        df.reset_index(drop=True, inplace=True)

        return df
