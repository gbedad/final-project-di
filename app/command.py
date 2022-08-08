import click
from flask.cli import with_appcontext

from app import db
from app.auth.models import User, MyInformation, MoreAboutMe, Upload, Subjects, SubjectPossible, SubjectsGrades, SubjectToStudy, Grades, GradesPossible, Interviews, Tutoring, Students, ModalitiesPossible, Modalities, Availabilities, Course


@click.command(name="create_tables")
@with_appcontext
def create_tables():
    db.create_all()
