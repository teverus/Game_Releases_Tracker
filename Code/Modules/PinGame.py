from datetime import datetime

TITLE = 0
PIN_STATUS = 2

PIN = " Pin "
UNPIN = "Unpin"

PINNED = "###"
FREE = "   "
TODAY = ">>>"

NEW_STATUS = {
    PIN: UNPIN,
    UNPIN: PIN,
}
NEW_INDICATION = {
    FREE: PINNED,
    PINNED: FREE,
    TODAY: PINNED,
}


class PinGame:
    def __init__(self, game_title, main):
        # === VARIABLES ================================================================
        self.title = game_title
        self.main = main
        self.df = main.database.read_table()
        self.target_index = self.get_target_index()

        # === ACTIONS ==================================================================
        self.change_pin_button()
        self.change_game_title()

    ####################################################################################
    #    ACTIONS                                                                       #
    ####################################################################################
    def change_pin_button(self):
        pinned_status = self.main.table.rows[self.target_index][PIN_STATUS]
        new_status = NEW_STATUS[pinned_status]

        self.main.table.rows[self.target_index][PIN_STATUS] = new_status

    def change_game_title(self):
        title = self.main.table.rows[self.target_index][TITLE]
        pinned_status = title[:3]
        new_status = NEW_INDICATION[pinned_status]
        is_released_today = self.get_if_released_today()
        new_status = TODAY if new_status == FREE and is_released_today else new_status

        self.main.table.rows[self.target_index][TITLE] = f"{new_status} {title[4:]}"

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
        indicated_date = self.main.table.rows[self.target_index][TITLE][5:16]

        day = datetime.today().strftime("%d").rjust(2, "0")
        month = datetime.today().strftime("%b").upper()
        year = datetime.today().strftime("%Y")
        today = f"{day} {month.capitalize()} {year}"

        result = indicated_date == today

        return result
