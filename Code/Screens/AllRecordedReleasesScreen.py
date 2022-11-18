from pathlib import Path

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import Screen, Action, SCREEN_WIDTH
from Code.TeverusSDK.Table import Table


class AllRecordedReleasesScreen(Screen):
    def __init__(self):
        self.database = DataBase(Path("Files/GameReleases.db"))
        self.df = self.database.read_table()
        self.recorded_months = set(self.df)

        self.actions = [
            Action(),
        ]

        self.table = Table(
            table_title="All recorded releases",
            rows=["Hello", "World"],
            rows_bottom_border=False,
            table_width=SCREEN_WIDTH,
        )

        super(AllRecordedReleasesScreen, self).__init__(self.table, self.actions)
