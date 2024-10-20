import reflex as rx

from project.styles import text

navbar: dict[str, str] = {
    "width": "100%",
    "padding": "1em 1.15em",
    "justify_content": "flex-start",  # Align the logo to the left
    "bg": rx.color_mode_cond(
        "rgba(255, 255, 255, 0.81)",
        "rgba(18, 17, 19, 0.81)",
    ),
    "align_items": "center",
    "border_bottom": "none",  # Remove the border
}


def render_navbar():
    return rx.hstack(
        rx.text(
            "GROUNDTRUTH.",
            font_family="Helvetica Neue LT Std",
            font_size="2em",
            font_weight="bold",
            color="black",
            padding="1em",
            text_align="left",  # Align text to the left
        ),
        **navbar,
    )

