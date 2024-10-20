import reflex as rx
from project.state import State
from typing import List
import json
import httpx
import os
from project.components.navbar import render_navbar
import reflex as rx
from project.state import State
from typing import List
import asyncio

class Update(rx.Base):
    commit_id: str
    commit_message: str
    relevant_doc: str
    doc_url: str
    code_summary: str
    doc_updates: str | None

class RecentUpdatesState(State):
    updates: List[Update] = []
    selected_update: Update = None
    last_update_time: float = 0

    async def fetch_recent_updates(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("http://localhost:8000/api/recent-updates")
                response.raise_for_status()
                data = response.json()
            return [Update(**item) for item in data], asyncio.get_event_loop().time()
        except Exception as e:
            print(f"Error fetching recent updates: {e}")
            return [], asyncio.get_event_loop().time()

    async def get_recent_updates(self):
        new_updates, update_time = await self.fetch_recent_updates()
        self.updates = new_updates
        self.last_update_time = update_time

    @rx.background
    async def poll_for_updates(self):
        while True:
            await asyncio.sleep(2)  # Poll every 5 seconds
            new_updates, update_time = await self.fetch_recent_updates()
            async with self:
                self.updates = new_updates
                self.last_update_time = update_time

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
            RecentUpdatesState.updates[::-1],  # Reverse the order of updates
            lambda update: rx.button(
                update.commit_message,
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
            on_mount=[
                RecentUpdatesState.get_recent_updates,
                RecentUpdatesState.poll_for_updates
            ],
            width="100%",
            height="100vh",
        ))
