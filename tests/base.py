# tests/base.py


from flask.ext.testing import TestCase

from project.server import app, db
from project.server.models import Student, Teacher, Admin


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('project.server.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        studentUser = Student(
            email="student@student.com",
            password="student_user"
        )
        db.session.add(studentUser)
        teacherUser = Teacher(
            email="teacher@teacher.com",
            password="teacher_user"
        )
        db.session.add(teacherUser)
        teacherUserTwo = Teacher(
            email="michael@teacher.com",
            password="teacher_user"
        )
        db.session.add(teacherUserTwo)
        adminUser = Admin(
            email="admin@admin.com",
            password="admin_user",
        )
        db.session.add(adminUser)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
