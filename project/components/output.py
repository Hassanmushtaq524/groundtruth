import reflex as rx

from project.components.drawer import render_drawer


def render_output():
    return rx.center(
        rx.cond(
            False,  # Always false to skip rendering the table
            rx.vstack(
                render_drawer(),
                # The table and its components have been removed
                width="100%",
                overflow="auto",
                padding="2em 2em",
            ),
            rx.spacer(),
        ),
        flex="60%",
        bg=rx.color_mode_cond(
            "#faf9fb",
            "#1a181a",
        ),
        border_radius="10px",
        overflow="auto",
    )
