from flashcards import db


class Folder(db.Model):
    __tablename__ = "folder"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("cards_user.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("folders"), cascade="delete")

    def __repr__(self):
        return f"<Folder {self.name}>"

    @classmethod
    def find_by_user_id(cls, folder_id, user_id):
        return Folder.query.filter_by(id=folder_id, user_id=user_id).first()

    @classmethod
    def find_by_id(cls, folder_id):
        return cls.query.filter_by(id=folder_id).first()
