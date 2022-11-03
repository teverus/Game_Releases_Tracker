import os
from math import ceil

import bext
from colorama import Back, Fore
from pandas import DataFrame

HIGHLIGHT = Back.WHITE + Fore.BLACK
END_HIGHLIGHT = Back.BLACK + Fore.WHITE


class ColumnWidth:
    FULL = "Full"
    FIT = "Fit"


class Table:
    def __init__(
        self,
        # Rows
        rows,
        rows_top_border="=",
        rows_bottom_border="=",
        rows_centered=True,
        # Table title
        table_title="",
        table_title_centered=True,
        table_title_caps=True,
        table_title_top_border="=",
        # General table
        table_width=None,
        highlight=None,
        highlight_footer=None,
        current_page=1,
        max_rows=None,
        max_columns=None,
        column_widths=None,
        # Footer
        footer=None,
        footer_centered=True,
        footer_bottom_border="=",
        footer_actions=None,
    ):
        """
        [rows]
            * A list of a list of lists
            * Example: ["a", "b", "c", "d"] or [["a", "b"], ["c", "d"]]
        [column_widths]
            * A dict where key is column index and value is ColumnWidth.FIT or FULL
            * Example: {0: ColumnWidth.FIT, 1: ColumnWidth.FULL}
        [highlight]
            * A list of coordinates [x, y], where x - rows, y - columns
            * Coordinates start from top left - [0, 0]
            * Set False to remove highlight
            * If None, it will be set to [0, 0] is a Table object is sent to Screen
            * Example: [1, 2] - highlights second row third column
        [footer_actions]
            * A list of Action, imported from Screen
            * Example: [Action(name="[Q] Exit", function=do_nothing, go_back=True)]
        [footer_bottom_border]
            * Used to print the lowest border of the table
            * Set to empty string ("") if you want it to disappear
        """
        # === General settings
        self.highlight = highlight
        self.highlight_footer = highlight_footer
        self.max_rows = max_rows if max_rows else len(rows)
        self.max_columns = max_columns if max_columns else self.get_max_columns(rows)
        self.several_columns_expected = self.get_several_columns_expected(rows)
        self.current_page = current_page

        # === Table title
        self.table_title = table_title
        self.table_title_centered = table_title_centered
        self.table_title_caps = table_title_caps
        self.table_title_top_border = table_title_top_border

        # === Rows
        self.rows_raw = rows
        self.max_rows_raw = max_rows
        self.max_page = self.get_max_page()
        self.rows = self.get_rows()
        self.rows_top_border = rows_top_border
        self.rows_bottom_border = rows_bottom_border
        self.rows_centered = rows_centered

        # === Footer
        self.footer_raw = footer
        self.footer_actions = footer_actions
        self.footer = self.get_footer()
        self.footer_bottom_border = footer_bottom_border
        self.footer_centered = footer_centered

        # Calculated values
        self.table_width = self.get_table_width(table_width)
        self.df = self.get_df()
        self.column_widths = self.get_column_widths(column_widths)
        self.border_length = self.get_border_length()
        self.cage = self.get_cage()
        self.pagination = self.get_pagination()

    def print_table(self):

        os.system("cls")
        bext.hide()

        # Table title top border
        if self.table_title and self.table_title_top_border:
            print(self.table_title_top_border * self.border_length)

        # Table title
        if self.table_title:
            centered = self.table_title_centered
            caps = self.table_title_caps
            self.table_title = self.table_title.upper() if caps else self.table_title
            tt = self.table_title.center if centered else self.table_title.ljust
            print(tt(self.border_length))

        # Rows top border
        if self.rows_top_border:
            print(self.rows_top_border * self.border_length)

        # Rows
        self.df = self.get_df()
        self.highlight = self.adjust_highlight_if_needed()
        for row in range(len(self.df)):
            a_row = []
            for column in range(self.max_columns):
                width = self.column_widths[column]
                data = self.df.iloc[row, column]
                data = data.center if self.rows_centered else data.ljust
                data = data(width, " ")
                if len(data) > width:
                    data = data[: -abs((len(data) - width) + 3)]
                    data = f"{data}..."
                highlighted = f"{HIGHLIGHT}{data}{END_HIGHLIGHT}"
                data = highlighted if [row, column] == self.highlight else data
                a_row.append(data)
            print(f" {' | '.join(a_row)} ")

        # Rows bottom border
        if self.rows_bottom_border:
            print(self.rows_bottom_border * self.border_length)

        # Footer
        if self.footer:
            footer = self.get_footer()

            for index, line in enumerate(footer):
                line = line.center if self.footer_centered else line.ljust
                line = line(self.border_length - 2)
                if self.highlight_footer:
                    highlighted = f"{HIGHLIGHT}{line}{END_HIGHLIGHT}"
                    is_highlighted = index == self.highlight_footer[0] - len(self.df)
                    line = highlighted if is_highlighted else line
                print(f" {line} ")

            if self.footer_bottom_border:
                print(self.footer_bottom_border * self.border_length)

        # Adjust the cage after the table has been recreated
        self.cage = self.get_cage()

    # ==================================================================================
    # === Helper class methods =========================================================
    # ==================================================================================

    def get_df(self):
        proper_rows = [r if isinstance(r, list) else [r] for r in self.get_rows()]
        max_columns = len(proper_rows[0])
        max_rows = len(proper_rows)

        df = DataFrame([], columns=[number for number in range(max_columns)])

        for row_index in range(max_rows):
            df.loc[row_index] = proper_rows[row_index]

        return df

    def get_column_widths(self, target_widths):
        actual_width = self.table_width - (((self.max_columns - 1) * 3) + 2)
        column_widths = {}

        if not target_widths:
            target_widths = {i: ColumnWidth.FULL for i in range(self.max_columns)}

        fit_cols = {k: v for k, v in target_widths.items() if v == ColumnWidth.FIT}
        full_cols = {k: v for k, v in target_widths.items() if v == ColumnWidth.FULL}
        expected_widths = {**fit_cols, **full_cols}

        full_target_length = None
        for col_index, width_type in expected_widths.items():
            if self.table_width:
                if width_type == ColumnWidth.FIT:
                    target_length = max(
                        [
                            len(row[col_index]) if isinstance(row, list) else len(row)
                            for row in self.rows
                        ]
                    )

                else:
                    if not full_target_length:
                        already_used = sum([v for v in column_widths.values()])
                        remaining = actual_width - already_used
                        number_of_full_cols = len(full_cols)
                        if remaining % number_of_full_cols == 0:
                            full_target_length = int(remaining / number_of_full_cols)
                        else:
                            extra = remaining % number_of_full_cols
                            proper_width = self.table_width - extra
                            raise Exception(f"Please use table_width = {proper_width}")
                    target_length = full_target_length

                column_widths[col_index] = target_length
            else:
                raise NotImplementedError("\n\nUse table_width!")

        return column_widths

    def get_border_length(self):
        if self.table_width:
            return self.table_width
        else:
            return ((self.max_columns - 1) * 3) + 2 + sum(self.column_widths.values())

    def get_cage(self):
        x_axis = [number for number in range(len(self.df))]
        y_axis = [number for number in range(len(self.df.columns))]

        coordinates = []
        for x in x_axis:
            for y in y_axis:
                coordinates.append([x, y])

        return coordinates

    def get_pagination(self):
        go_next = [[row, self.max_columns] for row in range(self.max_rows)]
        go_prev = [[row, -1] for row in range(self.max_rows)]

        return {1: go_next, -1: go_prev}

    def print(self):
        self.print_table()

    def get_footer_pages(self):
        if self.max_page:
            arrow_l = "    " if self.current_page == 1 else "<<< "
            short_l = "    " if self.current_page == 1 else "[Z] "

            arrow_r = "    " if self.current_page == self.max_page else " >>>"
            short_r = "    " if self.current_page == self.max_page else " [X]"

            current_page = f"{self.current_page:02}"
            max_page = f"{self.max_page:02}"
            return f"{short_l}{arrow_l}[{current_page}/{max_page}]{arrow_r}{short_r}"

        return None

    def get_footer(self):
        actions = [i.name for i in self.footer_actions] if self.footer_actions else None
        pages = self.get_footer_pages()

        if any([actions, pages]):
            actions = actions if actions is not None else []
            pages = [pages] if pages is not None else []

            return actions + pages

        return None

    def get_max_page(self):
        if self.max_rows_raw is None:
            return None

        elif self.max_rows_raw is not None and self.several_columns_expected:
            return ceil(len(self.rows_raw) / self.max_rows)

        else:
            return ceil(len(self.rows_raw) / (self.max_rows * self.max_columns))

    def get_rows(self):
        if self.max_rows_raw and not self.several_columns_expected:
            size = self.max_rows * self.max_columns
            previous_page = self.current_page - 1
            pack = self.rows_raw[size * previous_page : size * self.current_page]

            rows = []

            for col in range(self.max_columns):
                for row in range(self.max_rows):
                    if col == 0:
                        try:
                            rows.append([pack[row]])
                        except IndexError:
                            rows.append([""])
                    else:
                        try:
                            rows[row].append(pack[row + (self.max_rows * col)])
                        except IndexError:
                            rows[row].append("")

            return rows

        elif self.max_rows_raw:
            size = self.max_rows
            previous_page = self.current_page - 1

            return self.rows_raw[size * previous_page : size * self.current_page]

        else:
            return self.rows_raw

    def adjust_highlight_if_needed(self):
        if self.highlight:
            x, y = self.highlight
            max_length = len(self.df) - 1

            highlight = [max_length, y] if x > max_length else [x, y]

            return highlight

    @staticmethod
    def get_max_columns(rows):
        return max([len(row) if isinstance(row, list) else len([row]) for row in rows])

    @staticmethod
    def get_several_columns_expected(rows):
        row = rows[0]
        proper_row = len(row) if isinstance(row, list) else len([row])

        return proper_row != 1

    def get_table_width(self, expected_width):
        known_lengths = []
        side_padding = 2

        if expected_width:
            return expected_width

        if self.table_title:
            table_width = len(self.table_title)
            known_lengths.append(table_width + side_padding)

        if self.max_columns == 1:
            max_row = max([len(row) for row in self.rows])
            known_lengths.append(max_row + side_padding)

        else:
            max_row = max([sum([len(e) for e in row]) for row in self.rows])
            walls = (len(self.rows[0]) - 1) * 3
            known_lengths.append(max_row + walls + side_padding)

        table_width = max(known_lengths)

        return table_width
