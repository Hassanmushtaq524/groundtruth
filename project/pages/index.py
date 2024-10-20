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
        rx.heading("Recent Updates"),
        rx.button("Fetch Updates", on_click=RecentUpdatesState.get_recent_updates),
        rx.foreach(
            RecentUpdatesState.updates,
            lambda update: rx.box(
                rx.text("Commit ID: ", update.commit_id),
                rx.text("Commit Message: ", update.commit_message),
                rx.text("Relevant Doc: ", update.relevant_doc),
                rx.link("Doc URL: ", update.doc_url, href=update.doc_url, is_external=True),
                rx.text("Code Summary: ", update.code_summary),
                rx.text("Doc Updates: ", update.doc_updates),
                padding="1em",
                border="1px solid #ccc",
                margin="1em",
            )
        )
    )

# Update the page definition
@rx.page("/")
def index():
    return rx.vstack(
        rx.heading("Welcome to the Documentation Updater"),
        recent_updates_component()
    )
