from Code.Modules.ChangeGameStatus import ChangeGameStatus
from Code.Modules.OpenInSteam import OpenInSteam
from Code.TeverusSDK.Screen import Action, SCREEN_WIDTH, GO_BACK, do_nothing, Key
from Code.TeverusSDK.Table import Table, ColumnWidth


class ShowHiddenReleases:
    def __init__(self, main):
        action_name, hidden_status, index = self.get_opposite_action(main)

        actions = main.get_actions(remove_hidden=hidden_status, main=main)
        table = main.get_table(actions, main)

        main.actions = actions
        main.table = table
        main.table.footer[index].name = action_name

    ####################################################################################
    #    HELPERS
    ####################################################################################

    @staticmethod
    def get_opposite_action(main):
        footer = main.table.footer
        name = 0
        status = 1

        opposite = {
            main.SHOW_HIDDEN: [main.EXCLUDE_HIDDEN, False],
            main.EXCLUDE_HIDDEN: [main.SHOW_HIDDEN, True],
        }

        show_action = [a for a in footer if a.name == main.SHOW_HIDDEN]
        hide_action = [a for a in footer if a.name == main.EXCLUDE_HIDDEN]
        current_action = [a for a in [show_action, hide_action] if a][0][0]
        current_action = current_action.name

        action_name = opposite[current_action][name]
        hidden_status = opposite[current_action][status]
        index = [i for i, a in enumerate(footer) if a.name == current_action][0]

        return action_name, hidden_status, index
