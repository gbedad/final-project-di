
from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


"""course_table = db.Table('course_table',
                               db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                               db.Column('tutor_id', db.Integer, db.ForeignKey('user.id')))


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    subject = db.Column(db.String(32))
    tutor = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    student = db.Column(db.Integer, db.ForeignKey('student.id'), primary_key=True)
    course_day = db.Column(db.String(32))
    start_time = db.Column(db.String(10))
    end_time = db.Column(db.String(10))
    status = db.Column(db.String(32), deafult='created')

    @property
    def create_course_id(self):
        course_id = self.student + self.tutor + self.subject + self.course_day+self
        return course_id

    def __repr__(self):
        return f'<Course ID: {self.course_id}'"""
