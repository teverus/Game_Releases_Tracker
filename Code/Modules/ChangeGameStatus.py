from Code.TeverusSDK.Screen import show_message


class ChangeGameStatus:
    def __init__(self, game_title, main, status):
        self.df = main.database.read_table()
        self.title = game_title
        self.game_is_hidden = status

        self.write_changes_to_db(main)
        self.apply_changes_to_table(main)

        target_state = "unhidden" if self.game_is_hidden else "hidden"
        show_message(f'Release of "{self.title}" is now {target_state}')

    ####################################################################################
    #    PRIMARY ACTIONS                                                               #
    ####################################################################################

    def write_changes_to_db(self, main):
        index = self.df.loc[self.df.Title == self.title].index.values[0]
        target_status = "1" if not self.game_is_hidden else "0"
        self.df.loc[index, "Hidden"] = target_status
        main.database.write_to_table(self.df)

    def apply_changes_to_table(self, main):
        self.change_table_title(main)
        self.change_table_rows(main)

    ####################################################################################
    #    HELPERS                                                                       #
    ####################################################################################

    def get_target_index(self, main):
        for row_index, row in enumerate(main.table.visible_rows):
            row = [row] if not isinstance(row, list) else row
            for element in row:
                if self.title in element:
                    return row_index

    def change_table_rows(self, main):
        target_index = self.get_target_index(main)

        if self.game_is_hidden:
            main.actions[target_index][1].name = "  Hide  "
            main.table.rows[target_index][1] = "  Hide  "

        else:
            del main.table.rows[target_index]
            del main.actions[target_index]

            if not main.table.rows and not main.actions:
                main.table.set_nothing_to_show_state()

        x, y = main.table.highlight
        main.table.highlight = [x, 0]

        main.table.has_multiple_pages = main.table.get_multiple_pages()
        main.table.max_page = main.table.get_max_page()

    def change_table_title(self, main):
        if not self.game_is_hidden:
            old_number = int(main.table.table_title.split("[")[-1].split("]")[0])
            delta = -1 if not self.game_is_hidden else 1
            new_number = old_number + delta
            new_title = main.table.table_title.replace(str(old_number), str(new_number))
            main.table.table_title = new_title
