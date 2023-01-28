from flashcards import db


class Card(db.Model):
    __tablename__ = "card"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(255), unique=True, nullable=False)
    definition = db.Column(db.String(255), unique=True, nullable=False)
    set_id = db.Column(db.Integer, db.ForeignKey('set.id', ondelete='cascade'))
    learned = db.Column(db.Boolean, nullable=False, default=False)
    learned_at = db.Column(db.DateTime, nullable=True)
    sentences = db.relationship('Sentence', backref='card')

    def __repr__(self):
        return f"<Card {self.id}>"

    @classmethod
    def find_by_id(cls, set_id):
        return cls.query.filter_by(id=set_id).first()
