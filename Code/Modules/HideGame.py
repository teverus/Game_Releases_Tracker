from pathlib import Path

from Code.TeverusSDK.DataBase import DataBase
from Code.TeverusSDK.Screen import show_message, wait_for_key, Key


class HideGame:
    def __init__(self, game_title, main):
        database = DataBase(Path("Files/GameReleases.db"))
        df = database.read_table()
        game_title = game_title.strip().split(" | ")[-1]

        index = df.loc[df.Title == game_title].index.values[0]
        df.loc[index, "Hidden"] = 1
        database.write_to_table(df)

        target_index = None
        for row_index, row in enumerate(main.table.rows_raw):
            row = [row] if not isinstance(row, list) else row
            for element in row:
                if game_title in element:
                    target_index = row_index
                    break

        if target_index is not None:
            del main.table.rows_raw[target_index]
        else:
            raise Exception(f"Couldn't find {game_title} in\n{main.table.rows_raw = }")

        show_message(f'Release of "{game_title}" is now hidden')

        print('\n Press "Enter" to continue...')
        wait_for_key(Key.ENTER)
