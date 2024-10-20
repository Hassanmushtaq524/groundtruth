import reflex as rx
from project.pages import *
from backend.api import app as fastapi_app 
from dotenv import load_dotenv


app = rx.App(theme=rx.theme(
    appearance="light"
))

app.api = fastapi_app

if __name__ == "__main__":
    app.run()