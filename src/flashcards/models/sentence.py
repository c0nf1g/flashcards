from flashcards import db


class Sentence(db.Model):
    __tablename__ = "sentence"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(255), unique=True, nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id', ondelete='cascade'), nullable=False)

    def __repr__(self):
        return f"<Sentence {self.id}>"

    @classmethod
    def find_by_id(cls, set_id):
        return cls.query.filter_by(id=set_id).first()
