from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64), default='supervisor')
    status = db.Column(db.String(64), default="basic")
    upload_id = db.Column(db.Integer, db.ForeignKey('upload.id'))
    my_info = db.relationship('MyInformation', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return f'<User : {self.username}>'


class MyInformation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(120))
    city = db.Column(db.String(64))
    zipcode = db.Column(db.String(32))
    email2 = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    birth_date = db.Column(db.String(32))
    short_text = db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cv_filename = db.Column(db.String(100))
    cv_data = db.Column(db.LargeBinary)
    b3_filename = db.Column(db.String(100))
    b3_data = db.Column(db.LargeBinary)
    id_filename = db.Column(db.String(100))
    id_data = db.Column(db.LargeBinary)
    users = db.relationship('User', backref='upload', lazy='dynamic')