import msvcrt
import os

import bext
from colorama import Back, Fore

from Code.TeverusSDK.Table import Table

HIGHLIGHT = Back.WHITE + Fore.BLACK
END_HIGHLIGHT = Back.BLACK + Fore.WHITE

SCREEN_WIDTH = 99
GO_BACK = "[Q] Go back    "


class Screen:
    def __init__(self, table: Table, actions: list):
        """
        [table]
            * Must be an instance of Table
        [actions]
            * A list of one or more instances of Action, imported from this file
        """

        self.table = table
        self.actions = actions

        if self.table.highlight is None:
            self.table.highlight = [0, 0]

        # Clear screen and hide the cursor
        os.system("cls")
        bext.hide()

        # Print the table
        self.table.print()

        # Start the infinite loop
        while True:

            # [1] Check if there is an immediate action
            immediate_action = self.get_immediate_action()

            # [2-1] Get action ready if there is an immediate action
            if immediate_action:
                action = immediate_action

            # [2-2] or Wait for user input
            else:
                highlight, h_footer, action = self.get_user_action()
                self.table.highlight, self.table.highlight_footer = highlight, h_footer

            # [3] If an action is required, perform the action
            if action:

                # [3-0] Go back if a shortcut is pressed
                if isinstance(action, Action) and action.is_shortcut and action.go_back:
                    break

                # [3-1-1] Choose an action from the table if there is one
                if not immediate_action and self.table.highlight:
                    action = self.get_table_action()

                    if not isinstance(action, Action):
                        continue

                # [3-1-2] Choose an action from the footer
                elif not immediate_action and not self.table.highlight:
                    action = self.get_footer_action()

                # [3-2] Perform the action
                action()

                # [3-3] If the action ends this screen, do it
                if action.go_back:
                    break

            # [4] Print the table with the new parameters
            self.table.print()

    def get_user_action(self):
        # Declare major variables that will be returned
        highlight = self.table.highlight
        highlight_footer = self.table.highlight_footer
        action = False

        # A set of coordinates
        mv = {Key.DOWN: (1, 0), Key.UP: (-1, 0), Key.RIGHT: (0, 1), Key.LEFT: (0, -1)}

        # Shortcut keys
        shortcut = [
            # Go back
            Key.Q,
            Key.Q_RU,
            # Previous page
            Key.Z,
            Key.Z_RU,
            # Next page
            Key.X,
            Key.X_RU,
        ]

        # Get user input
        user_input = msvcrt.getch()

        # If the user pressed "Enter"
        if user_input == Key.ENTER:
            action = True

        # If the user pressed one of the arrow keys
        elif user_input in mv.keys():

            # Get the new position based on the user input
            new_pos = self.get_new_position(mv[user_input])

            # Check if the next/previous page was invoked
            page_change = self.get_page_change(new_pos)

            # Check if footer actions are involved
            footer_positions = self.get_footer_positions()

            # [1] Show next/previous page if the user moved to it
            if page_change:
                highlight = self.change_page(highlight, new_pos)

            # [2] Highlight footer if the user reaches the footer
            elif footer_positions and new_pos[0] in footer_positions:
                highlight = None
                highlight_footer = new_pos

            # [3] Do not move if the use tries to go below footer actions
            elif self.table.highlight_footer and new_pos[0] > max(footer_positions):
                pass

            # [4] Replace the current position with the new position if everything is OK
            elif new_pos in self.table.cage:
                highlight = new_pos
                highlight_footer = None if highlight_footer else highlight_footer

        # If the user pressed one of the shortcut keys
        elif user_input in shortcut:
            if user_input in [Key.Q, Key.Q_RU]:
                action = Action(go_back=True, is_shortcut=True)
            elif user_input in [Key.Z, Key.Z_RU]:
                if self.table.current_page != 1:
                    self.table.current_page -= 1
            elif user_input in [Key.X, Key.X_RU]:
                if self.table.current_page != self.table.max_page:
                    self.table.current_page += 1
            else:
                raise NotImplemented(f"{user_input = }")

        return highlight, highlight_footer, action

    def get_page_change(self, newpos):
        try:
            page_change = any([newpos in v for v in self.table.pagination.values()])
        except AttributeError:
            page_change = None

        return page_change

    def get_footer_positions(self):
        footer_positions = False

        if self.table.footer_actions:
            t_len = len(self.table.df) - 1
            f_len = len(self.table.footer_actions)
            footer_positions = [t_len + num for num in range(1, f_len + 1)]

        return footer_positions

    def change_page(self, highlight, newpos):
        delta = [k for k, v in self.table.pagination.items() if newpos in v]
        assert len(delta) == 1, "Delta goes both directions!"
        delta = delta[0]

        go_below = self.table.current_page == 1 and delta == -1
        go_over = self.table.current_page == self.table.max_page and delta == 1
        within_boundaries = not go_below and not go_over

        x, y = highlight
        if within_boundaries and delta == 1:
            highlight = [x, 0]
            self.table.current_page += 1

        elif within_boundaries and delta == -1:
            highlight = [x, self.table.max_columns - 1]
            self.table.current_page -= 1

        return highlight

    def get_new_position(self, delta):
        move_within_footer = not self.table.highlight and self.table.highlight_footer
        highlight_footer = self.table.highlight_footer

        if move_within_footer and delta[1] != 0:
            new_position = self.table.highlight_footer

        elif move_within_footer and delta[0] != 0:
            new_position = [c1 + c2 for c1, c2 in zip(highlight_footer, delta)]

        else:
            new_position = [c1 + c2 for c1, c2 in zip(self.table.highlight, delta)]

        return new_position

    def get_immediate_action(self):
        target_list = self.actions

        if isinstance(self.actions[0], list):
            sub_actions = []
            [[sub_actions.append(sa) for sa in action] for action in self.actions]
            target_list = sub_actions

        immediate_action = [action for action in target_list if action.immediate_action]

        if immediate_action:
            assert len(immediate_action) == 1, "\n[ERROR] Too many immediate actions!!!"

            return immediate_action[0]

    def get_table_action(self):
        this_page = self.table.current_page - 1
        next_page = this_page + 1
        max_rows = self.table.max_rows
        predefined_cols = isinstance(self.actions[0], list)

        if not predefined_cols:
            pack = self.table.max_rows * self.table.max_columns
            available_actions = self.actions[this_page * pack : next_page * pack]

            index = 0
            actions = []
            for col in range(self.table.max_columns):
                for row in range(max_rows):
                    try:
                        specific_action = available_actions[index]
                    except IndexError:
                        break
                    if self.table.max_columns == 1:
                        actions.append(specific_action)
                    else:
                        try:
                            actions[row].append(specific_action)
                        except IndexError:
                            actions.append([])
                            actions[row].append(specific_action)
                    index += 1
        else:
            actions = self.actions[this_page * max_rows : next_page * max_rows]

        # Get the right action
        x, y = self.table.highlight
        try:
            action = actions[x][y]
        except TypeError:
            action = actions[x]
        except IndexError:
            action = None

        return action

    def get_footer_action(self):
        x, _ = self.table.highlight_footer
        table_length = len(self.table.df)
        target_index = x - table_length

        return self.table.footer_actions[target_index]


########################################################################################
#    CLASSES RELATED TO SCREEN                                                         #
########################################################################################


class Action:
    def __init__(
        self,
        name=None,
        function=None,
        arguments=None,
        immediate_action=False,
        go_back=False,
        is_shortcut=False,
    ):
        self.name = name
        self.function = function
        self.arguments = arguments
        self.immediate_action = immediate_action
        self.go_back = go_back
        self.is_shortcut = is_shortcut

    def __call__(self, *args, **kwargs):
        if self.arguments:
            self.function(**self.arguments)
        else:
            self.function()


class Key:
    DOWN = b"P"
    UP = b"H"
    RIGHT = b"M"
    LEFT = b"K"

    ENTER = b"\r"

    Q = b"q"
    Q_RU = b"\xa9"
    Z = b"z"
    Z_RU = b"\xef"
    X = b"x"
    X_RU = b"\xe7"


########################################################################################
#    HELPER FUNCTIONS                                                                  #
########################################################################################


def do_nothing():
    pass


def wait_for_key(target_key):
    key = msvcrt.getch()
    while key != target_key:
        key = msvcrt.getch()


def show_message(message, border=" ", centered=True, upper=True):
    print(HIGHLIGHT)
    print(f"{border * SCREEN_WIDTH}")
    message = message.upper() if upper else message
    text = message.center if centered else message.ljust
    print(text(SCREEN_WIDTH))
    print(f"{border * SCREEN_WIDTH}{END_HIGHLIGHT}")
