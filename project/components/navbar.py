import reflex as rx

navbar: dict[str, str] = {
    "width": "100%",
    "padding": "70px",
    "justify_content": "flex-start",  # Align the logo to the left
    "align_items": "center",
    "border_bottom": "none",  # Remove the border
}

def return_to_home():
    return rx.redirect("/")

def render_navbar():
    return rx.hstack(
        rx.text(
            "GROUNDTRUTH.",
            font_family="Helvetica Neue LT Std",
            font_size="2em",
            font_weight="bold",
            color="black",
            text_align="left",  # Align text to the left
            on_click=return_to_home
        ),
        **navbar,
    )

