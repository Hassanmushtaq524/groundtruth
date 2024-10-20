"""The dashboard page."""

import reflex as rx
from project.state import State

from project.components.navbar import render_navbar
from project.components.query import render_query_component
from project.components.output import render_output
from project.states.queries import QueryAPI

class DashboardState(State):
    repo_link: str = ""

    def navigate_to_next_page(self):
        return rx.redirect("/next_page")

def render_getting_started_text():
    return rx.box(
        rx.hstack(
            rx.vstack(
                rx.text(
                    "GETTING",
                    font_family="Helvetica Neue LT Std",
                    font_size="150px",
                    font_weight="35",
                    color="black",
                    line_height="1",
                ),
                rx.text(
                    "STARTED",
                    font_family="Helvetica Neue LT Std",
                    font_size="150px",
                    font_weight="35",
                    color="#C48DFF",
                    line_height="1",
                ),
                spacing="0",
                align_items="flex-start",
                padding_left="70px",  # Adjusted for 30px left movement
                padding_top="0px",
            ),
            rx.vstack(
                rx.box(
                    rx.text(
                        "The way to",
                        font_family="Helvetica Neue LT Std",
                        font_size="31px",  # Reduced font size by 5px
                        font_weight="45",
                        color="black",
                        line_height="1",
                        class_name="typing-effect",  # Add a class for the typing effect
                    ),
                    rx.text(
                        "edit your documentation_",
                        font_family="Helvetica Neue LT Std",
                        font_size="31px",  # Reduced font size by 5px
                        font_weight="45",
                        color="black",
                        line_height="1",
                        class_name="typing-effect",  # Add a class for the typing effect
                    ),
                    spacing="0",
                    align_items="flex-start",
                    padding_top="0px",
                ),
                spacing="0",
                align_items="flex-start",
                padding_left="20px",  # Adjusted for 30px left movement
            ),
            spacing="20px",
            align_items="flex-start",
        ),
        width="100%",
        display="flex",
        justify_content="flex-start",
        align_items="center",
        margin_left="-30px",  # Move the "GETTING STARTED" text 30px to the left
    )

def render_link_repository_box():
    return rx.hstack(
        rx.input(
            placeholder="Link your repository",
            value=DashboardState.repo_link,
            on_change=DashboardState.set_repo_link,
            font_family="Helvetica Neue LT Std",
            font_size="32px",
            color="#787777",
            width="521px",
            height="56px",
            border="2px solid #C48DFF",
            border_radius="12px",
            box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
            padding_left="10px",
        ),
        rx.button(
            rx.icon(
                tag="chevron-right",
                color="white",
                font_size="32px",
                font_weight="bold",
            ),
            bg="#C48DFF",
            color="white",
            border_radius="12px",
            height="56px",
            width="56px",
            _hover={"bg": "#A76FE3"},
            box_shadow="0 4px 8px rgba(196, 141, 255, 0.3)",
            on_click=DashboardState.navigate_to_next_page,
        ),
        spacing="4",
        margin_top="20px",
        margin_left="50px",
    )

@rx.page("/", on_load=QueryAPI.run_get_request)
def dashboard() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        render_navbar(),  # Keep the "GROUNDTRUTH" text in place
        rx.box(
            render_getting_started_text(),
            width="100%",
            height="100%",
            display="flex",
            justify_content="flex-start",
            align_items="center",
            margin_top="130px",
        ),
        render_link_repository_box(),  # Add the new box here
        rx.hstack(
            render_query_component(),
            render_output(),
            width="100%",
            display="flex",
            flex_wrap="wrap",
            spacing="6",
            padding="2em 1em",
            margin_left="-30px",  # Move the query and output components 30px to the left
        ),
        spacing="4",
        display="flex",
    )

@rx.page("/next_page")
def next_page():
    return rx.vstack(
        rx.heading("Next Page"),
        rx.text("This is an empty page for now."),
    )
