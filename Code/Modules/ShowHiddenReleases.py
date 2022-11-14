from Code.Modules.HideGame import HideGame
from Code.Modules.OpenInSteam import OpenInSteam
from Code.TeverusSDK.Screen import Action, SCREEN_WIDTH, GO_BACK, do_nothing, Key
from Code.TeverusSDK.Table import Table, ColumnWidth


class ShowHiddenReleases:
    def __init__(self, main):
        action_name, hidden_status, index = self.get_opposite_action(main)

        rows = main.get_rows(remove_hidden=hidden_status)

        actions = [
            [
                Action(
                    name=row,
                    function=OpenInSteam,
                    arguments={"game_title": row},
                ),
                Action(
                    name="Hide",
                    function=HideGame,
                    arguments={"game_title": row, "main": main},
                ),
            ]
            for row in rows
        ]

        current_page = main.table.current_page
        highlight = main.table.highlight

        table = Table(
            table_title="This month's releases",
            rows=[[action[0].name, action[1].name] for action in actions],
            table_width=SCREEN_WIDTH,
            max_rows=29,
            current_page=current_page,
            highlight=highlight,
            column_widths={0: ColumnWidth.FIT, 1: ColumnWidth.FULL},
            footer=[
                Action(
                    name=GO_BACK,
                    function=do_nothing,
                    go_back=True,
                    shortcut=[Key.Q, Key.Q_RU],
                ),
                Action(
                    name="[S] Show hidden",
                    function=ShowHiddenReleases,
                    arguments={"main": main},
                    shortcut=[Key.S, Key.S_RU],
                ),
            ],
        )

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

        opposite_name = {
            main.SHOW_HIDDEN: [main.EXCLUDE_HIDDEN, False],
            main.EXCLUDE_HIDDEN: [main.SHOW_HIDDEN, True],
        }

        show_action = [a for a in footer if a.name == main.SHOW_HIDDEN]
        hide_action = [a for a in footer if a.name == main.EXCLUDE_HIDDEN]
        current_action = [a for a in [show_action, hide_action] if a][0][0]

        action_name = opposite_name[current_action.name][name]
        hidden_status = opposite_name[current_action.name][status]
        index = [i for i, a in enumerate(footer) if a.name == current_action.name][0]

        return action_name, hidden_status, index
