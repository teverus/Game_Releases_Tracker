from pathlib import Path

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.ScreenV2 import show_message


class HideGame:
    def __init__(self, game_title, main):
        self.database = DataBase(Path("Files/GameReleases.db"))
        self.df = self.database.read_table()
        self.title = game_title.strip().split(" | ")[-1]

        self.write_changes_to_db()
        self.apply_changes_to_table(main)
        show_message(f'Release of "{self.title}" is now hidden')

    def write_changes_to_db(self):
        index = self.df.loc[self.df.Title == self.title].index.values[0]
        self.df.loc[index, "Hidden"] = 1
        self.database.write_to_table(self.df)

    def get_target_index(self, main):
        for row_index, row in enumerate(main.table.rows_raw):
            row = [row] if not isinstance(row, list) else row
            for element in row:
                if self.title in element:
                    return row_index

    def apply_changes_to_table(self, main):
        target_index = self.get_target_index(main)

        if target_index is not None:
            del main.table.rows_raw[target_index]
            del main.actions[target_index]
            x, _ = main.table.highlight
            main.table.highlight = [x, 0]
        else:
            raise Exception(f"No {self.title} in\n{main.table.rows_raw = }")
