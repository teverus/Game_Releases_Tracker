import msvcrt
import os

import bext

########################################################################################
#    SCREEN CONFIGS                                                                    #
########################################################################################
from Code.TeverusSDK.TableV2 import HIGHLIGHT, END_HIGHLIGHT

SCREEN_WIDTH = 99
GO_BACK = "[Q] Go back    "


########################################################################################
#    SCREEN CLASS                                                                      #
########################################################################################
class ScreenV2:
    def __init__(self, table, actions):
        """
        [table]
            * A mandatory parameter
            * An instance of Table()
        [actions]
            * A mandatory parameter
            * A list of instances of Action()
        [shortcuts]
            * An optional parameter
        """
        # For internal use only
        self.movement_keys = {
            Key.DOWN: (0, 1),
            Key.UP: (0, -1),
            Key.RIGHT: (1, 0),
            Key.LEFT: (-1, 0),
        }

        self.table = table
        self.actions = actions

        # Set default highlight position
        if self.table.highlight is None:
            self.table.highlight = [0, 0]

        # Print the table
        os.system("cls")
        bext.hide()
        self.table.print_table()

        # Start the infinite loop
        while True:
            # Get user action
            self.table.highlight, action = self.get_user_action()

            # Print the table with the new parameters
            self.table.print_table()

    ####################################################################################
    #   INTERNAL OPERATIONS                                                            #
    ####################################################################################
    def get_user_action(self):
        # Variables that will be returned
        highlight = self.table.highlight
        action = False

        # Get actual user input
        user_input = msvcrt.getch()

        if user_input != b"\x00":
            ...

        # If user chooses "Enter"
        if user_input == Key.ENTER:
            action = True

        # If user chooses one of the movement keys
        elif user_input in self.movement_keys:
            delta = self.movement_keys[user_input]
            new_position = [c1 + c2 for c1, c2 in zip(self.table.highlight, delta)]
            if new_position in self.table.cage:
                highlight = new_position

        return highlight, action


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
        """
        [arguments]
            * A dict where key is the name of the argument in the function,
            value - the actual value
            * Key and the name of the argument must be identical
            * Example: {"game_title": row}
        """
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

    S = b"s"
    S_RU = b"\xeb"


########################################################################################
#    HELPER FUNCTIONS                                                                  #
########################################################################################
def do_nothing():
    pass


def wait_for_key(target_key):
    key = msvcrt.getch()
    while key != target_key:
        key = msvcrt.getch()


def show_message(message, border=" ", centered=True, upper=True, wait_for_enter=True):
    print(HIGHLIGHT)
    print(f"{border * SCREEN_WIDTH}")
    message = message.upper() if upper else message
    text = message.center if centered else message.ljust
    print(text(SCREEN_WIDTH))
    print(f"{border * SCREEN_WIDTH}{END_HIGHLIGHT}")

    if wait_for_enter:
        print('\n Press "Enter" to continue...')
        wait_for_key(Key.ENTER)
