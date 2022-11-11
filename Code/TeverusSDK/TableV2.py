import os

import bext
from colorama import Back, Fore

HIGHLIGHT = Back.WHITE + Fore.BLACK
END_HIGHLIGHT = Back.BLACK + Fore.WHITE


class ColumnWidth:
    FULL = "Full"
    FIT = "Fit"


class TableV2:
    def __init__(
        self,
        # Rows
        rows: list[str] or list[list[str]],
        rows_top_border="=",
        rows_bottom_border="=",
        rows_centered=True,
        # Table title
        table_title="",
        table_title_centered=True,
        table_title_caps=True,
        table_title_top_border="=",
        # Footer
        footer=None,
        footer_centered=True,
        footer_bottom_border="=",
        # General table
        table_width=None,
        highlight=None,
        current_page=1,
        max_rows=None,
        max_columns=None,
        column_widths=None,
    ):
        """
        [rows]
            * Mandatory parameter, must be a list of strings or a list of lists
            * Example: ["a", "b", "c", "d"] or [["a", "b"], ["c", "d"]]
        """
        # Internal use only
        self.side_padding_length = 2
        self.wall_length = 3

        # Table title
        self.table_title = table_title
        self.table_title_top_border = table_title_top_border
        self.table_title_centered = table_title_centered
        self.table_title_caps = table_title_caps

        # Rows
        self.rows = self.get_rows(rows)
        self.rows_top_border = rows_top_border
        self.rows_bottom_border = rows_bottom_border
        self.rows_centered = rows_centered

        # Footer
        self.footer = footer
        self.footer_bottom_border = footer_bottom_border
        self.footer_centered = footer_centered

        # General table
        self.highlight = highlight
        self.current_page = current_page
        self.max_rows = self.get_max_rows(max_rows)
        self.max_columns = self.get_max_columns(max_columns)
        self.cage = self.get_cage()

        # Calculated values
        self.walls_length = (self.max_columns - 1) * self.wall_length
        self.visible_rows = self.get_visible_rows()
        self.table_width = self.get_table_width(table_width)
        self.column_widths = self.get_column_widths(column_widths)

    ####################################################################################
    #    PRINT TABLE                                                                   #
    ####################################################################################
    def print_table(self):

        # Clear the console
        os.system("cls")
        bext.hide()

        # Print table title if any
        if self.table_title:
            print(self.table_title_top_border * self.table_width)

            tt = self.table_title
            tt = tt.upper() if self.table_title_caps else tt
            tt = tt.center(self.table_width) if self.table_title_centered else tt
            print(tt)

        # Print rows top border if any
        if self.rows_top_border:
            print(self.rows_top_border * self.table_width)

        # Print rows, highlighting them if necessary
        self.visible_rows = self.get_visible_rows()
        for index_y, row in enumerate(self.visible_rows):
            line = []
            for index_x, cell in enumerate(row):
                target_width = self.column_widths[index_x]
                cell = cell.center(target_width) if self.rows_centered else cell
                highlighted = f"{HIGHLIGHT}{cell}{END_HIGHLIGHT}"
                data = highlighted if [index_x, index_y] == self.highlight else cell
                line.append(data)
            line = " | ".join(line)
            print(f" {line} ")

        # Print rows bottom border if any
        if self.rows_bottom_border:
            print(self.rows_bottom_border * self.table_width)

        # Print footer if any
        if self.footer:
            ...

    ####################################################################################
    #    TABLE CALCULATIONS                                                            #
    ####################################################################################
    @staticmethod
    def get_rows(rows):
        rows = [rows] if not isinstance(rows, list) else rows
        result = [[r] if not isinstance(r, list) else r for r in rows]

        return result

    def get_max_rows(self, max_rows):
        result = max_rows if max_rows else len(self.rows)

        return result

    def get_max_columns(self, max_columns):
        result = max_columns if max_columns else max([len(r) for r in self.rows])

        return result

    def get_table_width(self, expected_width):
        if expected_width:
            return expected_width

        known_lengths = []

        # Calculate the widest possible title length
        title_width = len(self.table_title) + self.side_padding_length
        known_lengths.append(title_width)

        # Calculate the widest possible row length
        max_row = max([sum([len(e) for e in row]) for row in self.visible_rows])
        max_row_length = max_row + self.walls_length + self.side_padding_length
        known_lengths.append(max_row_length)

        table_width = max(known_lengths)

        return table_width

    def get_column_widths(self, target_widths):
        actual_width = self.table_width - self.walls_length - self.side_padding_length
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
                    # target_length = max(
                    #     [
                    #         len(row[col_index]) if isinstance(row, list) else len(row)
                    #         for row in self.rows
                    #     ]
                    # )
                    ...
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

    def get_visible_rows(self):
        result = None

        if len(self.rows) > self.max_rows:
            ...

        else:
            result = self.rows

        return result

    def get_cage(self):
        x_axis = [number for number in range(self.max_columns)]
        y_axis = [number for number in range(self.max_rows)]

        coordinates = []
        for y in y_axis:
            for x in x_axis:
                coordinates.append([x, y])

        return coordinates
