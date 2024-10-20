import reflex as rx
from project.state import State
from typing import List
import json
import os

class Update(rx.Base):
    commit_id: str
    commit_message: str
    relevant_doc: str
    doc_url: str
    code_summary: str
    doc_updates: str

class RecentUpdatesState(State):
    updates: List[Update] = []
    selected_update: Update = None

    def get_recent_updates(self):
        try:
            # Adjust this path to the location of your updates.json file
            file_path = os.path.join(os.path.dirname(__file__), '../../', 'updates.json')
            with open(file_path, 'r') as f:
                data = json.load(f)
            self.updates = [Update(**item) for item in data]
        except Exception as e:
            print(f"Error fetching recent updates: {e}")
            self.updates = []

    def select_update(self, update_id: str):
        self.selected_update = next((u for u in self.updates if u.commit_id == update_id), None)

def sidebar_component():
    return rx.vstack(
        rx.heading("Commits", size="md", mb=4),
        rx.foreach(
            RecentUpdatesState.updates,
            lambda update: rx.button(
                update.commit_message,
                on_click=RecentUpdatesState.select_update(update.commit_id),
                width="100%",
                justify_content="flex-start",
                py=2,
                height="1.5rem",
                variant="ghost",
                font_size="1.4em",  # Increased font size
            )
        ),
        width="25vw",
        height="100%",
        padding="1em",
    )

def main_content():
    return rx.cond(
        RecentUpdatesState.selected_update,
        rx.vstack(
            rx.hstack(
                rx.heading(RecentUpdatesState.selected_update.commit_message, size="lg", mb=4),
                rx.text(
                    RecentUpdatesState.selected_update.commit_id[:7],  # Display first 7 characters of commit ID
                    color="#A0AEC0",  # Light gray color for better visibility
                    font_size="0.875em",  # Equivalent to "sm", but more explicit
                    align_self="flex-end",
                    ml="0.5rem"  # More precise margin-left value
                ),
            ),
            rx.markdown(RecentUpdatesState.selected_update.code_summary, mb=2),
            rx.link(f"Updates to {RecentUpdatesState.selected_update.relevant_doc} Documentation", href=RecentUpdatesState.selected_update.doc_url, is_external=True, font_weight="bold", font_size="2em"),
            rx.markdown(RecentUpdatesState.selected_update.doc_updates),
            align_items="start",
            spacing="0.5em",
            width="100%",
            padding="2em",
        ),
        rx.text("Select a commit from the sidebar to view details.", font_style="italic"),
    )

# Update the page definition
@rx.page("/")
def index():
    return rx.hstack(
        sidebar_component(),
        main_content(),
        on_mount=RecentUpdatesState.get_recent_updates,
        width="100%",
        height="100vh",
    )
