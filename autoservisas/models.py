from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from sqlalchemy import DateTime
from autoservisas import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    e_mail = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)

    def __repr__(self) -> str:
        return self.vardas

class LimitedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

