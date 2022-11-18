from datetime import datetime
from pathlib import Path

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import (
    Screen,
    Action,
    SCREEN_WIDTH,
    do_nothing,
    GO_BACK_ACTION,
)
from Code.TeverusSDK.Table import Table


class AllRecordedReleasesScreen(Screen):
    def __init__(self):
        self.database = DataBase(Path("Files/GameReleases.db"))
        self.df = self.database.read_table()
        self.recorded_months = [
            datetime.strptime(date, "%b %Y").strftime("%B %Y")
            for date in list(set(self.df.MonthAndYear))
        ]

        self.actions = [
            Action(
                name=month,
                function=do_nothing,
            )
            for month in self.recorded_months
        ]

        self.table = Table(
            table_title="All recorded releases",
            rows=[action.name for action in self.actions],
            max_rows=29,
            table_width=SCREEN_WIDTH,
            footer=[GO_BACK_ACTION],
        )

        super(AllRecordedReleasesScreen, self).__init__(self.table, self.actions)
