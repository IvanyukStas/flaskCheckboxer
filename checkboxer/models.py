from werkzeug.security import generate_password_hash, check_password_hash

from checkboxer import db


class Users(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    user_name: str = db.Column(db.String(64), index=True, unique=True)
    password_hash: str = db.Column(db.String(128))

    def __repr__(self):
        return f'User: {self.user_name}'


    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)


    def check_assword(self, password: str):
       return check_password_hash(self.password_hash, password)