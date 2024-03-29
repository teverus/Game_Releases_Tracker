from datetime import datetime

TITLE = 0
PIN_STATUS = 2

PIN = " Pin "
UNPIN = "Unpin"

PINNED = "###"
FREE = "   "
TODAY = ">>>"

BOOL_TO_PIN = {"0": "1", "1": "0"}

NEW_STATUS = {
    PIN: UNPIN,
    UNPIN: PIN,
}
NEW_INDICATION = {
    FREE: PINNED,
    PINNED: FREE,
    TODAY: PINNED,
}


class ChangePinStatus:
    def __init__(self, game_title, main):
        # === VARIABLES ================================================================
        self.title = game_title
        self.main = main
        self.df = main.database.read_table()
        self.target_index = self.get_target_index()

        # === ACTIONS ==================================================================
        self.change_pin_button()
        self.change_game_title()
        self.change_pinned_status_in_db()

    ####################################################################################
    #    ACTIONS                                                                       #
    ####################################################################################
    def change_pin_button(self):
        pinned_status = self.main.table.visible_rows[self.target_index][PIN_STATUS]
        new_status = NEW_STATUS[pinned_status]

        self.main.table.visible_rows[self.target_index][PIN_STATUS] = new_status

    def change_game_title(self):
        title = self.main.table.visible_rows[self.target_index][TITLE]
        pinned_status = title[:3]
        new_st = NEW_INDICATION[pinned_status]
        is_released_today = self.get_if_released_today()
        new_st = TODAY if new_st == FREE and is_released_today else new_st

        self.main.table.visible_rows[self.target_index][TITLE] = f"{new_st} {title[4:]}"

    def change_pinned_status_in_db(self):
        index = self.df.loc[self.df.Title == self.title].index.values[0]
        current_pinned_status = self.df.loc[index, "Pinned"]
        new_pinned_status = BOOL_TO_PIN[current_pinned_status]

        self.df.loc[index, "Pinned"] = new_pinned_status

        self.main.database.write_to_table(self.df)

    ####################################################################################
    #    HELPERS                                                                       #
    ####################################################################################

    def get_target_index(self):
        for row_index, row in enumerate(self.main.table.visible_rows):
            row = [row] if not isinstance(row, list) else row
            for element in row:
                if self.title in element:
                    return row_index

    def get_if_released_today(self):
        indicated_date = self.main.table.visible_rows[self.target_index][TITLE][5:16]

        day = datetime.today().strftime("%d").rjust(2, "0")
        month = datetime.today().strftime("%b").upper()
        year = datetime.today().strftime("%Y")
        today = f"{day} {month.capitalize()} {year}"

        result = indicated_date == today

        return result
