import os

from flashcards import create_app, db
from flashcards.models.user import User

app = create_app(os.getenv("FLASK_ENV", "development"))


@app.shell_context_processor
def shell():
    return {"db": db, "User": User}
