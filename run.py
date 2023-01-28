import os

from flashcards import create_app, db
from flashcards.models import User, BlacklistedToken, Set, Card, Sentence

app = create_app(os.getenv("FLASK_ENV", "development"))


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "User": User,
        "BlacklistedToken": BlacklistedToken,
        "Set": Set,
        "Card": Card,
        "Sentence": Sentence
    }
