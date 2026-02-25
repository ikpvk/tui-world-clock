from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DataTable
from textual.containers import Container
from textual.reactive import reactive

from state import AppState
from screens.add_timezone import AddTimezoneScreen


class WorldClockApp(App):

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("t", "toggle_time_format", "Toggle 12/24h"),
        ("d", "delete_clock", "Delete"),
        ("a", "add_clock", "Add"),
    ]

    CSS = """
    Screen {
        align: center middle;
    }

    DataTable {
        width: 80%;
        height: auto;
    }

    AddTimezoneScreen {
        align: center middle;
    }
    """

    refresh_toggle = reactive(True)

    def __init__(self):
        super().__init__()
        self.state = AppState()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            DataTable(id="clock_table")
        )
        yield Footer()

    def on_mount(self):
        table = self.query_one("#clock_table", DataTable)

        table.add_columns("Label", "Time", "UTC Offset", "Timezone")
        table.cursor_type = "row"

        self.refresh_table()
        self.set_interval(1, self.refresh_table)

    def refresh_table(self):
        table = self.query_one("#clock_table", DataTable)

        current_row = table.cursor_row

        table.clear()

        for clock in self.state.clocks:
            table.add_row(
                clock.label,
                clock.get_time(self.state.format_24h),
                clock.get_utc_offset(),
                clock.zone
            )

        if current_row is not None and current_row < len(self.state.clocks):
            table.move_cursor(row=current_row)

    def action_toggle_time_format(self):
        self.state.format_24h = not self.state.format_24h
        self.state.config["format_24h"] = self.state.format_24h
        self.state.config_manager.save(self.state.config)
        self.refresh_table()

    def action_delete_clock(self):
        table = self.query_one("#clock_table", DataTable)
        row = table.cursor_row

        if row is not None:
            self.state.remove_clock(row)
            self.refresh_table()

    def action_add_clock(self):
        def on_result(result):
            if result:
                raw = result.split("/")[-1]
                label = raw.replace("_", " ").title()

                self.state.add_clock(label, result)
                self.refresh_table()

        self.push_screen(AddTimezoneScreen(), on_result)

    def action_quit(self):
        self.exit()


if __name__ == "__main__":
    app = WorldClockApp()
    app.run()
