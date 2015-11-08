# tests/base.py


from flask.ext.testing import TestCase

from project import app, db
from project.models import User


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        studentUser = User(
            email="student@student.com",
            password="student_user",
            student=True,
            teacher=False,
            admin=False
        )
        db.session.add(studentUser)
        teacherUser = User(
            email="teacher@teacher.com",
            password="teacher_user",
            student=False,
            teacher=True,
            admin=False
        )
        db.session.add(teacherUser)
        teacherUserTwo = User(
            email="michael@teacher.com",
            password="teacher_user",
            student=False,
            teacher=True,
            admin=False
        )
        db.session.add(teacherUserTwo)
        adminUser = User(
            email="admin@admin.com",
            password="admin_user",
            student=False,
            teacher=False,
            admin=True
        )
        db.session.add(adminUser)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
