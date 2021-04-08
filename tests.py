import unittest
from checkboxer.models import Users
from unittest import TestCase
from config import Config
from checkboxer import app, db





class UserModelTests(TestCase):
    def setUp(self) -> None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()


    def tearDown(self) -> None:
        db.session.remove()
        db.drop_all()


    def test_password_hashing(self):
        u = Users(user_name='test')
        u.set_password('`123456')
        self.assertFalse(u.check_assword('asdf'))
        self.assertTrue((u.check_assword('`123456')))


if __name__ == '__main__':
    unittest.main(verbosity=2)