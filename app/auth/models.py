from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


subject_grade_table = db.Table('grades_table',
                               db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id')),
                               db.Column('grade_id', db.Integer, db.ForeignKey('grades.id')))

subjects_table = db.Table('all_subjects',
                              db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                              db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id')))

users_table = db.Table('all_users',
                              db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                              db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64), default='supervisor')
    status = db.Column(db.String(64), default="1")
    upload_id = db.Column(db.Integer, db.ForeignKey('upload.id'))
    my_info = db.relationship('MyInformation', backref='user', uselist=False)
    more = db.relationship('MoreAboutMe', backref='user', uselist=False)
    tutoring_exp = db.relationship('Tutoring', backref='user', uselist=False)
    user_subjects = db.relationship('Subjects', secondary=subjects_table, back_populates='all_users')
    my_interviews = db.relationship('Interviews', backref='user', uselist=False)

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


class Tutoring(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    maths = db.Column(db.String(120))
    physics = db.Column(db.String(120))
    svt = db.Column(db.String(120))
    french = db.Column(db.String(120))
    english = db.Column(db.String(120))
    spanish = db.Column(db.String(120))
    history = db.Column(db.String(120))
    geopolitics = db.Column(db.String(120))
    modalities = db.Column(db.String(240))
    engagement = db.Column(db.String(32))
    start_date = db.Column(db.String(32))
    end_date = db.Column(db.String(32))
    frequency = db.Column(db.Integer)
    monday = db.Column(db.String(32))
    tuesday = db.Column(db.String(10))
    wednesday = db.Column(db.String(10))
    thursday = db.Column(db.String(10))
    friday = db.Column(db.String(10))
    sunday = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    def __repr__(self):
        return f'<Tutoring : {self.engagement}>'


class MoreAboutMe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    why = db.Column(db.String(120))
    when = db.Column(db.String(64))
    inquiry = db.Column(db.String(32))
    experience = db.Column(db.String(32))
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


class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(32))
    grades_a = db.relationship('Grades', secondary=subject_grade_table, back_populates='subjects_a')
    all_users = db.relationship('User', secondary=users_table, back_populates='user_subjects')


class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(db.String(32))
    subjects_a = db.relationship('Subjects', secondary=subject_grade_table, back_populates='grades_a')


class Interviews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interview_date = db.Column(db.String(32))
    interviewer = db.Column(db.String(32))
    is_accepted = db.Column(db.Boolean)
    message = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    def accepted(self):
        if self.is_accepted is True:
            return True

    def proposed(self):
        if self.interview_date is not None:
            return True

    def done(self):
        if self.message is not None:
            return True


