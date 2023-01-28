from flashcards import db


class Card(db.Model):
    __tablename__ = "card"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    term = db.Column(db.Text, nullable=False)
    definition = db.Column(db.Text, nullable=False)
    learned = db.Column(db.Boolean, nullable=False, default=False)
    folder_id = db.Column(db.Integer, db.ForeignKey("folder.id"), nullable=False)
    folder = db.relationship("Folder", backref=db.backref("cards"), cascade="delete")

    def __repr__(self):
        return f"<Card {self.term}>"

    @classmethod
    def find_by_id(cls, card_id):
        return cls.query.filter_by(id=card_id).first()
