import datetime

from app import db, login_manager, flask_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import app.course.models as mod
from sqlalchemy.sql import func

import time
import jwt


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


tutor_course_table = db.Table('association_tutor_course',
                              db.Column('tutor_id', db.ForeignKey('user.id')),
                              db.Column('course_id', db.ForeignKey('course.id')))

student_course_table = db.Table('association_student_course',
                              db.Column('student_id', db.ForeignKey('students.id')),
                              db.Column('course_id', db.ForeignKey('course.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(64), default='supervisor')
    status = db.Column(db.String(64), default="1")
    #upload_id = db.Column(db.Integer, db.ForeignKey('upload.id'))
    my_upload_cv = db.relationship('UploadCv', backref='user', uselist=False)
    my_upload_b3 = db.relationship('UploadB3', backref='user', uselist=False)
    my_upload_id = db.relationship('UploadId', backref='user', uselist=False)
    my_info = db.relationship('MyInformation', backref='user', uselist=False)
    more = db.relationship('MoreAboutMe', backref='user', uselist=False)
    tutoring_exp = db.relationship('Tutoring', backref='user', uselist=False)
    user_subjects = db.relationship('Subjects', secondary=subjects_table, back_populates='all_users')
    my_interviews = db.relationship('Interviews', backref='user', uselist=False)
    courses = db.relationship('Course', secondary=tutor_course_table, back_populates='tutor')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        timeout = time.time() + expires_in
        payload = {
            'reset_password': self.id,
            'exp': timeout
        }

        # Get the secret key from config
        secret_key = flask_app.config['SECRET_KEY']

        # Create the token
        token = jwt.encode(payload, secret_key, algorithm="HS256")

        # Turn it to string
        s_token = token

        return s_token

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, flask_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

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
    modalities = db.Column(db.String(240))
    engagement = db.Column(db.String(32))
    start_date = db.Column(db.String(32))
    end_date = db.Column(db.String(32))
    frequency = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    tutor_availabilities = db.relationship('Availabilities', backref='tutor')
    tutor_modalities = db.relationship('Modalities', backref='tutor')
    tutor_subjects = db.relationship('SubjectsGrades', backref='tutor')

    def __repr__(self):
        return f'<Tutoring : {self.engagement}>'


class MoreAboutMe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    why = db.Column(db.String(250))
    when = db.Column(db.String(250))
    inquiry = db.Column(db.String(64))
    experience = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)


class UploadCv(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cv_filename = db.Column(db.String(100))
    cv_data = db.Column(db.LargeBinary)
    #users = db.relationship('User', backref='upload', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)


class UploadB3(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    b3_filename = db.Column(db.String(100))
    b3_data = db.Column(db.LargeBinary)
    #users = db.relationship('User', backref='upload', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)


class UploadId(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_filename = db.Column(db.String(100))
    id_data = db.Column(db.LargeBinary)
    #users = db.relationship('User', backref='upload', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)


class Subjects(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(32))
    grades_a = db.relationship('Grades', secondary=subject_grade_table, back_populates='subjects_a')
    all_users = db.relationship('User', secondary=users_table, back_populates='user_subjects')


class SubjectsGrades(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(32))
    grade_from = db.Column(db.String(32))
    grade_to = db.Column(db.String(32))
    user_subjects_owner = db.Column(db.Integer, db.ForeignKey('tutoring.id'))


class Grades(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade = db.Column(db.String(32))
    subjects_a = db.relationship('Subjects', secondary=subject_grade_table, back_populates='grades_a')


class Interviews(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interview_date = db.Column(db.String(64))
    interview_time = db.Column(db.String(32))
    interviewer = db.Column(db.String(32))
    is_accepted = db.Column(db.Boolean)
    message = db.Column(db.String(100))
    is_done = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    def accepted(self):
        if self.is_accepted is True:
            return True

    def proposed(self):
        if self.interview_date is not None:
            return True

    def done(self):
        if self.is_done is not None:
            return True


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    email = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    phone_parents = db.Column(db.String(32))
    street = db.Column(db.String(32))
    city = db.Column(db.String(32))
    zipcode = db.Column(db.String(32))
    school = db.Column(db.String(32))
    grade = db.Column(db.String(32), default='')
    modality = db.Column(db.String(32), default='')
    student_subjects = db.relationship('SubjectToStudy', backref='student')
    student_availabilities = db.relationship('Availabilities', backref='student')
    courses = db.relationship('Course', secondary=student_course_table, back_populates='student')

    def __repr__(self):
        return f'<Student : {self.first_name} {self.last_name}>'


class Modalities(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    modality = db.Column(db.String(32))
    user_modality_owner = db.Column(db.Integer, db.ForeignKey('tutoring.id'))

    def __repr__(self):
        return f'<Modality : {self.modality}>'


class ModalitiesPossible(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    modality = db.Column(db.String(32))

    def __repr__(self):
        return f'<Modality : {self.modality}>'


class GradesPossible(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    grade_name = db.Column(db.String(32))

    def __repr__(self):
        return f'<Grade : {self.grade_name}>'


class SubjectToStudy(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_name = db.Column(db.String(32))
    subject_owner = db.Column(db.Integer, db.ForeignKey('students.id'))

    def __repr__(self):
        return f'<Subject : {self.subject_name}>'


class SubjectPossible(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_name = db.Column(db.String(32))

    def __repr__(self):
        return f'<Subject : {self.subject_name}>'


class Availabilities(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day_possible = db.Column(db.String(32))
    day_time_from = db.Column(db.String(32))
    day_time_to = db.Column(db.String(32))
    availability_owner = db.Column(db.Integer, db.ForeignKey('students.id'))
    user_avail_owner = db.Column(db.Integer, db.ForeignKey('tutoring.id'))

    def __repr__(self):
        return f'<Availabilities : {self.day_possible} from {self.day_time_from} to {self.day_time_to}>'


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    student = db.relationship('Students', secondary=student_course_table, back_populates='courses')
    tutor = db.relationship('User', secondary=tutor_course_table, back_populates='courses')
    subject = db.Column(db.String(32))
    selected_day = db.Column(db.String(32))
    start_time = db.Column(db.String(10))
    end_time = db.Column(db.String(10))
    status = db.Column(db.String(32), default='created')

    @property
    def set_course_id(self):
        return f"{self.student}-{self.tutor}-{self.subject}"

    def __repr__(self):
        return f'<Course ID: {self.subject} {self.selected_day}>'


