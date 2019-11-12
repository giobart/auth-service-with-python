from random import randint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

DATABASE_NAME = 'sqlite:///auth.db'

db = SQLAlchemy()


class User(db.Model):
    '''
    Models the user of the application.
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Unicode(128), unique=True, nullable=False)
    email = db.Column(db.Unicode(128), unique=True, nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    dateofbirth = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        salt = randint(16, 32)
        self.password = generate_password_hash(password, salt_length=salt)

    def check_password(self, password):
        match = check_password_hash(self.password, password)
        return match

    def get_id(self):
        return self.id

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }

        return {'users': list(map(lambda x: to_json(x), User.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}
