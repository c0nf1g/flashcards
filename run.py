import os

from flashcards import create_app

app = create_app(os.getenv("FLASK_ENV", "development"))
