from datetime import datetime, timezone, timedelta
from uuid import uuid4

import jwt
from flashcards import db, bcrypt
from flashcards.models.token_blacklist import BlacklistedToken
from flashcards.utils.datetime_util import utc_now
from flashcards.utils.result import Result
from flask import current_app


class User(db.Model):
    __tablename__ = "cards_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(45), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, default=utc_now)
    password_hash = db.Column(db.String(128), nullable=False)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid4()))
    sets = db.relationship('Set', backref='cards_user')

    def __repr__(self):
        return f"<User {self.username}>"

    @property
    def password(self):
        raise AttributeError("Password is a write-only field")

    @password.setter
    def password(self, password):
        log_rounds = current_app.config.get("BCRYPT_LOG_ROUNDS")
        hash_bytes = bcrypt.generate_password_hash(password, log_rounds)
        self.password_hash = hash_bytes.decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def encode_access_token(self):
        now = datetime.now(timezone.utc)
        token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
        token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
        expire = now + timedelta(hours=token_age_h, minutes=token_age_m)
        if current_app.config["TESTING"]:
            expire = now + timedelta(seconds=5)
        payload = dict(exp=expire, iat=now, sub=self.public_id)
        key = current_app.config.get("SECRET_KEY")
        return jwt.encode(payload, key, algorithm="HS256")

    @staticmethod
    def decode_access_token(access_token):
        if access_token.startswith("Bearer "):
            split = access_token.split("Bearer")
            access_token = split[1].strip()
        try:
            key = current_app.config.get("SECRET_KEY")
            payload = jwt.decode(access_token, key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            error = "Access token expired."
            return Result.Fail(error)
        except jwt.InvalidTokenError:
            error = "Invalid token."
            return Result.Fail(error)

        if BlacklistedToken.check_blacklist(access_token):
            error = "Token is blacklisted. Please log in again."
            return Result.Fail(error)

        user_dict = dict(
            public_id=payload["sub"], token=access_token, expires_at=payload["exp"]
        )

        return Result.Ok(user_dict)

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
