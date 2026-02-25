from textual.widgets import Input, Static, DataTable
from textual.containers import Vertical
from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual import events

from timezone_manager import TimezoneManager


class AddTimezoneScreen(ModalScreen):

    BINDINGS = [
        ("escape", "app.pop_screen", "Cancel"),
    ]

    def __init__(self):
        super().__init__()
        self.tz_manager = TimezoneManager()
        self.filtered = []

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Search Timezone:"),
            Input(placeholder="Type to search...", id="search_input"),
            DataTable(id="results_table"),
        )

    def on_mount(self):
        table = self.query_one("#results_table", DataTable)
        table.add_columns("Timezone")
        table.cursor_type = "row"

        self.update_results("")

        # Focus input by default
        self.query_one("#search_input", Input).focus()

    def update_results(self, query):
        table = self.query_one("#results_table", DataTable)
        table.clear()

        self.filtered = self.tz_manager.search(query)

        for tz in self.filtered:
            table.add_row(tz)

        if self.filtered:
            table.move_cursor(row=0)

    def on_input_changed(self, event: Input.Changed):
        self.update_results(event.value)

    def on_key(self, event: events.Key):
        table = self.query_one("#results_table", DataTable)
        input_box = self.query_one("#search_input", Input)

        # If arrow down pressed while in input → move focus to table
        if event.key == "down" and input_box.has_focus:
            table.focus()
            event.stop()

        # If arrow up at top of table → move back to input
        elif event.key == "up" and table.has_focus and table.cursor_row == 0:
            input_box.focus()
            event.stop()

        # Enter selects current row
        elif event.key == "enter" and table.has_focus:
            if self.filtered and table.cursor_row is not None:
                selected_zone = self.filtered[table.cursor_row]
                self.dismiss(selected_zone)
                event.stop()
