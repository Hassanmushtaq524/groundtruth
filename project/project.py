import reflex as rx
from project.pages import *
from backend.api import app as fastapi_app 

class State(rx.State):
    """Define empty state to allow access to rx.State.router."""


app = rx.App()
app.api = fastapi_app

if __name__ == "__main__":
    app.run()