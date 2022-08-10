from datetime import timezone

from flashcards import db
from flashcards.utils.datetime_util import utc_now, dtaware_fromtimestamp


class BlacklistedToken(db.Model):
    __tablename__ = "token_blacklist"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, default=utc_now())
    expires_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, token, expires_at):
        self.token = token
        self.expires_at = dtaware_fromtimestamp(expires_at, use_tz=timezone.utc)

    @classmethod
    def check_blacklist(cls, token):
        exists = cls.query.filter_by(token=token).first()
        return True if exists else False
