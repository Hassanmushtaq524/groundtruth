import reflex as rx
from project.state import State
from typing import List
import json
import httpx
import os
from project.components.navbar import render_navbar

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

    async def get_recent_updates(self):
        try:
            # Make an asynchronous GET request to the server to fetch recent updates
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8001/api/recent-updates")
                response.raise_for_status()  # Raise an error for bad status codes
                data = response.json()
            
            # Parse the JSON data into Update objects
            self.updates = [Update(**item) for item in data]
        except Exception as e:
            print(f"Error fetching recent updates: {e}")
            self.updates = []

        # try:
        #     # Adjust this path to the location of your updates.json file
        #     file_path = os.path.join(os.path.dirname(__file__), '../../', 'updates.json')
        #     with open(file_path, 'r') as f:
        #         data = json.load(f)
        #     self.updates = [Update(**item) for item in data]
        # except Exception as e:
        #     print(f"Error fetching recent updates: {e}")
        #     self.updates = []

    def select_update(self, update_id: str):
        self.selected_update = next((u for u in self.updates if u.commit_id == update_id), None)

def sidebar_component():
    return rx.vstack(
        rx.heading("COMMITS", 
                   size="md", 
                   mb=4, 
                   color="black",
                   font_family="Helvetica Neue LT Std",
                   font_weight="bold"),
        rx.foreach(
            RecentUpdatesState.updates,
            lambda update: rx.button(
                update.commit_id,
                on_click=RecentUpdatesState.select_update(update.commit_id),
                width="100%",
                justify_content="flex-start",
                py=2,
                variant="ghost"
            )
        ),
        display="flex",
        gap="40px",
        width="fit-content",
        height="100vh",
        border_right="1px solid #C48DFF",
        padding="70px",
    )

def main_content():
    return rx.cond(
        RecentUpdatesState.selected_update,
        rx.vstack(
            rx.heading(RecentUpdatesState.selected_update.commit_message, size="lg", mb=4),
            rx.hstack(
                rx.text("Relevant Doc: ", font_weight="bold"),
                rx.link(
                    RecentUpdatesState.selected_update.relevant_doc,
                    href=RecentUpdatesState.selected_update.doc_url,
                    is_external=True
                ),
                width="100%",
            ),
            rx.text("Code Summary:", font_weight="bold"),
            rx.text(RecentUpdatesState.selected_update.code_summary, mb=2),
            rx.text("Doc Updates:", font_weight="bold"),
            rx.markdown(RecentUpdatesState.selected_update.doc_updates),
            align_items="start",
            spacing="0.5em",
            width="100%",
            padding="70px",
            color="black",
            height="100vh",
            overflow_y="scroll"
        ),
        rx.text("Select a commit from the sidebar to view details.", 
                    font_style="italic", 
                    color="black",
                    font_family="Helvetica Neue LT Std",
                    font_weight="bold",
                    padding="70px"),
    )

# Update the page definition
@rx.page("/changes")
def changes():
    return rx.vstack(        
        render_navbar(),
        rx.hstack(
            sidebar_component(),
            main_content(),
            on_mount=RecentUpdatesState.get_recent_updates,
            width="100%",
            height="100vh",
        ))
