# project/tests/base.py


from flask.ext.testing import TestCase

from project.server import app, db
from project.server.models import Student, Teacher, Admin


class BaseTestCaseAdmin(TestCase):

    def create_app(self):
        app.config.from_object('project.server.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        studentUser = Student(
            email='student@student.com',
            password='student_user'
        )
        db.session.add(studentUser)
        teacherUser = Teacher(
            email='teacher@teacher.com',
            password='teacher_user'
        )
        db.session.add(teacherUser)
        teacherUserTwo = Teacher(
            email='michael@teacher.com',
            password='teacher_user'
        )
        db.session.add(teacherUserTwo)
        adminUser = Admin(
            email='admin@admin.com',
            password='admin_user',
        )
        db.session.add(adminUser)
        db.session.commit()

        self.client.post(
            '/login',
            data=dict(
                email='admin@admin.com',
                password='admin_user',
                confirm='admin_user'
            ),
            follow_redirects=True
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class BaseTestCaseMain(TestCase):

    def create_app(self):
        app.config.from_object('project.server.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class BaseTestCaseStudent(TestCase):

    def create_app(self):
        app.config.from_object('project.server.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        studentUser = Student(
            email='student@student.com',
            password='student_user'
        )
        db.session.add(studentUser)
        teacherUser = Teacher(
            email='teacher@teacher.com',
            password='teacher_user'
        )
        db.session.add(teacherUser)
        teacherUserTwo = Teacher(
            email='michael@teacher.com',
            password='teacher_user'
        )
        db.session.add(teacherUserTwo)
        adminUser = Admin(
            email='admin@admin.com',
            password='admin_user',
        )
        db.session.add(adminUser)
        db.session.commit()

        self.client.post(
            '/login',
            data=dict(
                email='student@student.com',
                password='student_user',
                confirm='student_user'
            ),
            follow_redirects=True
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class BaseTestCaseTeacher(TestCase):

    def create_app(self):
        app.config.from_object('project.server.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        studentUser = Student(
            email='student@student.com',
            password='student_user'
        )
        db.session.add(studentUser)
        teacherUser = Teacher(
            email='teacher@teacher.com',
            password='teacher_user'
        )
        db.session.add(teacherUser)
        teacherUserTwo = Teacher(
            email='michael@teacher.com',
            password='teacher_user'
        )
        db.session.add(teacherUserTwo)
        adminUser = Admin(
            email='admin@admin.com',
            password='admin_user',
        )
        db.session.add(adminUser)
        db.session.commit()

        self.client.post(
            '/login',
            data=dict(
                email='teacher@teacher.com',
                password='teacher_user',
                confirm='teacher_user'
            ),
            follow_redirects=True
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()
