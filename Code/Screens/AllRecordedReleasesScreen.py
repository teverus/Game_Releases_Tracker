from datetime import datetime
from pathlib import Path

from Code.Screens.MonthsReleasesScreen import MonthsReleasesScreen
from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import (
    Screen,
    Action,
    SCREEN_WIDTH,
    GO_BACK_ACTION,
)
from Code.TeverusSDK.Table import Table


class AllRecordedReleasesScreen(Screen):
    def __init__(self):
        self.database = DataBase(Path("Files/GameReleases.db"))
        self.df = self.database.read_table()
        self.months_in_order = self.get_months_in_order()

        self.actions = [
            Action(
                name=month_and_year,
                function=MonthsReleasesScreen,
                arguments={"month_and_year": month_and_year},
            )
            for month_and_year in self.months_in_order
        ]

        self.table = Table(
            table_title="All recorded releases",
            rows=[action.name for action in self.actions],
            max_rows=29,
            table_width=SCREEN_WIDTH,
            footer=[GO_BACK_ACTION],
        )

        super(AllRecordedReleasesScreen, self).__init__(self.table, self.actions)

    ####################################################################################
    #    HELPERS                                                                       #
    ####################################################################################

    def get_months_in_order(self):
        recorded_months = [
            datetime.strptime(date, "%b %Y").strftime("%B %Y")
            for date in list(set(self.df.MonthAndYear))
        ]
        recorded_years = sorted(set([date.split()[-1] for date in recorded_months]))
        ordered_months = []

        for recorded_year in recorded_years:
            for month_number in range(1, 13):
                for mon in recorded_months:
                    if recorded_year in mon:
                        month_as_int = datetime.strptime(mon, "%B %Y").strftime("%m")
                        if int(month_as_int) == month_number:
                            ordered_months.append(mon)

        return ordered_months
