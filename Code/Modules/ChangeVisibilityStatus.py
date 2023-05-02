from math import ceil

from Code.TeverusSDK.Screen import show_message

HIDE = " Hide "
UNHIDE = "Unhide"


class ChangeVisibilityStatus:
    def __init__(self, game_title, main):
        self.title = game_title
        self.main = main
        self.target_index = self.get_target_index()
        self.df = main.database.read_table()
        self.game_is_currently_hidden = self.get_hidden_status()
        self.show_hidden_games = self.get_show_hidden_games()

        self.apply_changes_to_table(main)
        self.write_changes_to_db()

        target_state = "unhidden" if self.game_is_currently_hidden else "hidden"
        show_message(f'Release of "{self.title}" is now {target_state}')

    ####################################################################################
    #    PRIMARY ACTIONS                                                               #
    ####################################################################################

    def write_changes_to_db(self):
        index = self.df.loc[self.df.Title == self.title].index.values[0]
        target_status = "1" if not self.game_is_currently_hidden else "0"
        self.df.loc[index, "Hidden"] = target_status
        self.main.database.write_to_table(self.df)

    def apply_changes_to_table(self, main):
        self.change_table_title(main)
        self.change_table_rows(main)

    ####################################################################################
    #    HELPERS                                                                       #
    ####################################################################################

    def get_target_index(self):
        for row_index, row in enumerate(self.main.table.visible_rows):
            row = [row] if not isinstance(row, list) else row
            for element in row:
                if self.title in element:
                    return row_index

    def change_table_rows(self, main):
        rows_before = main.table.max_rows * (main.table.current_page - 1)
        adjusted_index = rows_before + self.target_index

        if self.game_is_currently_hidden:
            main.actions[adjusted_index][1].name = HIDE
            main.table.rows[adjusted_index][1] = HIDE

        elif not self.game_is_currently_hidden and self.show_hidden_games:
            main.actions[adjusted_index][1].name = UNHIDE
            main.table.rows[adjusted_index][1] = UNHIDE

        else:

            del main.table.rows[adjusted_index]
            del main.actions[adjusted_index]

            if not main.table.rows and not main.actions:
                main.table.set_nothing_to_show_state()

            max_page = ceil(len(main.table.rows) / main.table.max_rows)
            if max_page < main.table.max_page:
                if main.table.current_page > max_page:
                    main.table.current_page = max_page
                main.table.max_page = max_page

        x, y = main.table.highlight
        main.table.highlight = [x, 0]

        main.table.has_multiple_pages = main.table.get_multiple_pages()
        main.table.max_page = main.table.get_max_page()

    def change_table_title(self, main):
        if not self.game_is_currently_hidden and not self.show_hidden_games:
            old_number = int(main.table.table_title.split("[")[-1].split("]")[0])
            delta = -1 if not self.game_is_currently_hidden else 1
            new_number = old_number + delta
            new_title = main.table.table_title.replace(str(old_number), str(new_number))
            main.table.table_title = new_title

    def get_hidden_status(self):
        is_hidden = HIDE != self.main.table.visible_rows[self.target_index][1]

        return is_hidden

    def get_show_hidden_games(self):
        current_footer_filter = [a.name for a in self.main.table.footer][1]
        show_hidden_games = self.main.SHOW_HIDDEN != current_footer_filter

        return show_hidden_games
