from flashcards import db


class Card(db.Model):
    __tablename__ = "card"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(255), nullable=False)
    definition = db.Column(db.String(255), nullable=False)
    learned = db.Column(db.Boolean, nullable=False, default=False)
    learned_at = db.Column(db.DateTime, nullable=True)
    set_id = db.Column(db.Integer, db.ForeignKey('set.id'), nullable=False)
    set = db.relationship('Set', backref=db.backref('cards', cascade='delete'))
    sentences = db.relationship('Sentence', backref="card", cascade='delete')

    def __repr__(self):
        return f"<Card {self.id}>"

    @classmethod
    def find_by_id(cls, card_id):
        return cls.query.filter_by(id=card_id).first()

    @classmethod
    def find_by_set_id(cls, card_id, set_id):
        return cls.query.filter_by(id=card_id, set_id=set_id).first()
