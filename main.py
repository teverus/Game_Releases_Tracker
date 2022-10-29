from Code.Table import Table


class Application:
    def __init__(self):
        self.table = Table(
            table_title="This is a pig",
            rows=[["Hello", "1"], ["world", "This is not just any pig!"]],
        )
        self.table.print_table()
        a = 1


if __name__ == "__main__":
    Application()
