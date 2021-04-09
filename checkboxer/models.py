from werkzeug.security import generate_password_hash, check_password_hash

from checkboxer import db


class User(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    user_name: str = db.Column(db.String(64), index=True, unique=True)
    password_hash: str = db.Column(db.String(128))
    checkboxlists = db.relationship('Checkboxlist', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'User: {self.user_name}'


    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)


    def check_assword(self, password: str):
       return check_password_hash(self.password_hash, password)


class Checkboxlist(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    checkbox_list_title: str = db.Column(db.String(128), index=True)
    checkbox_privacy: bool = db.Column(db.Boolean, default=True, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    checkbox = db.relationship('Checkbox', backref='user_checkboxer', lazy='dynamic')

    def __repr__(self):
        return f'Checkbox: <{self.checkbox_title}>'


class Checkbox(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    checkbox_name: str = db.Column(db.String(128), index=True)
    checkbox_status: bool = db.Column(db.Boolean, default=False, nullable=False)
    checkbox_list = db.Column(db.Integer, db.ForeignKey('checkboxlist.id'))


    def __repr__(self):
        return f'Checkbox: <{self.checkbox_name}>'