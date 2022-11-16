from pathlib import Path

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import show_message


class ChangeGameStatus:
    def __init__(self, game_title, main, status):
        self.database = DataBase(Path("Files/GameReleases.db"))
        self.df = self.database.read_table()
        self.title = game_title
        self.is_hidden = status

        self.write_changes_to_db()
        self.apply_changes_to_table(main)

        target_state = "unhidden" if self.is_hidden else "hidden"
        show_message(f'Release of "{self.title}" is now {target_state}')

    def write_changes_to_db(self):
        index = self.df.loc[self.df.Title == self.title].index.values[0]
        target_status = "1" if not self.is_hidden else "0"
        self.df.loc[index, "Hidden"] = target_status
        self.database.write_to_table(self.df)

    def get_target_index(self, main):
        for row_index, row in enumerate(main.table.visible_rows):
            row = [row] if not isinstance(row, list) else row
            for element in row:
                if self.title in element:
                    return row_index

    def apply_changes_to_table(self, main):
        target_index = self.get_target_index(main)

        if self.is_hidden:
            main.actions[target_index][1].name = "  Hide  "
            main.table.rows[target_index][1] = "  Hide  "

        else:
            del main.table.rows[target_index]
            del main.actions[target_index]

        x, y = main.table.highlight
        main.table.highlight = [x, 0]

        # TODO !! Изменить количество в шапке
        ...
