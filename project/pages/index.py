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

def recent_updates_component():
    return rx.vstack(
        rx.heading("Recent Updates", size="lg", mb=4),
        rx.cond(
            RecentUpdatesState.updates,
            rx.foreach(
                RecentUpdatesState.updates,
                lambda update: rx.box(
                    rx.vstack(
                        rx.hstack(
                            rx.text("Commit ID: ", font_weight="bold"),
                            rx.text(update.commit_id),
                            width="100%",
                        ),
                        rx.text(update.commit_message, font_style="italic", mb=2),
                        rx.hstack(
                            rx.text("Relevant Doc: ", font_weight="bold"),
                            rx.link(update.relevant_doc, href=update.doc_url, is_external=True),
                            width="100%",
                        ),
                        rx.text("Code Summary:", font_weight="bold"),
                        rx.text(update.code_summary, mb=2),
                        rx.text("Doc Updates:", font_weight="bold"),
                        rx.text(update.doc_updates),
                        align_items="start",
                        spacing="0.5em",
                    ),
                    padding="1em",
                    border="1px solid #e0e0e0",
                    border_radius="md",
                    box_shadow="sm",
                    margin="1em",
                )
            ),
            rx.text("No updates available.", font_style="italic"),
        )
    )

# Update the page definition
@rx.page("/")
def index():
    return rx.vstack(
        rx.heading("Documentation Updater", size="2xl", mb=6),
        recent_updates_component(),
        on_mount=RecentUpdatesState.get_recent_updates,
        margin="0 auto",
        padding="2em",
        min_height="100vh",
    )
