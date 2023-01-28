from flashcards import db


class Set(db.Model):
    __tablename__ = "set"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('cards_user.id', ondelete='cascade'))
    cards = db.relationship('Card', backref='set')

    def __repr__(self):
        return f"<Set {self.name}>"

    @classmethod
    def find_by_id(cls, set_id):
        return cls.query.filter_by(id=set_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
