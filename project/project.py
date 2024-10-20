import reflex as rx
from project.pages import home, changes
from project.styles.styles import custom_theme
from backend.api import app as fastapi_app 
from dotenv import load_dotenv

style = {
    "background-color": "white"
}

app = rx.App(style=style, theme=custom_theme)

app.api = fastapi_app

if __name__ == "__main__":
    app.run()