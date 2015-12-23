# project/tests/user/test_user.py


import datetime
import unittest

from flask.ext.login import current_user

from project.tests.base import BaseTestCaseAdmin
from project.server import bcrypt
from project.server.models import User
from project.server.user.forms import LoginForm


class TestUserBlueprint(BaseTestCaseAdmin):

    def test_correct_login(self):
        # Ensure login behaves correctly with correct credentials.
        with self.client:
            self.client.get('/logout', follow_redirects=True)
            response = self.client.post(
                '/login',
                data=dict(
                    email='admin@admin.com',
                    password='admin_user'
                ),
                follow_redirects=True
            )
            self.assertIn(b'Welcome, <em>admin@admin.com</em>!', response.data)
            self.assertIn(
                b'<li><a href="/admin/dashboard/">Dashboard</a></li>',
                response.data
            )
            self.assertIn(b'Logout', response.data)
            self.assertTrue(current_user.email == 'admin@admin.com')
            self.assertTrue(current_user.is_active())
            self.assertEqual(response.status_code, 200)

    def test_logout_behaves_correctly(self):
        # Ensure logout behaves correctly - regarding the session.
        with self.client:
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You were logged out. Bye!', response.data)
            self.assertFalse(current_user.is_active)

    def test_logout_route_requires_login(self):
        # Ensure logout route requres logged in user.
        self.client.get('/logout', follow_redirects=True)
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    def test_validate_success_login_form(self):
        # Ensure correct data validates.
        form = LoginForm(email='admin@admin.com', password='admin_user')
        self.assertTrue(form.validate())

    def test_validate_invalid_email_format(self):
        # Ensure invalid email format throws error.
        form = LoginForm(email='unknown', password='example')
        self.assertFalse(form.validate())

    def test_get_by_id(self):
        # Ensure id is correct for the current/logged in user.
        with self.client:
            self.client.get('/logout', follow_redirects=True)
            self.client.post('/login', data=dict(
                email='admin@admin.com', password='admin_user'
            ), follow_redirects=True)
            self.assertTrue(current_user.id == 4)

    def test_registered_on_defaults_to_datetime(self):
        # Ensure that registered_on is a datetime.
        with self.client:
            user = User.query.filter_by(email='admin@admin.com').first()
            self.assertIsInstance(user.registered_on, datetime.datetime)

    def test_check_password(self):
        # Ensure given password is correct after unhashing.
        admin = User.query.filter_by(email='admin@admin.com').first()
        self.assertTrue(
            bcrypt.check_password_hash(admin.password, 'admin_user'))
        self.assertFalse(bcrypt.check_password_hash(admin.password, 'foobar'))

    def test_validate_invalid_password(self):
        # Ensure user can't login when the pasword is incorrect.
        with self.client:
            self.client.get('/logout', follow_redirects=True)
            response = self.client.post('/login', data=dict(
                email='admin@admin.com', password='foo_bar'
            ), follow_redirects=True)
        self.assertIn(b'Invalid email and/or password.', response.data)

    def test_register_route(self):
        # Ensure about route behaves correctly.
        response = self.client.get('/register', follow_redirects=True)
        self.assertIn(b'<h1>Please Register</h1>\n', response.data)

    def test_student_registration(self):
        # Ensure registration behaves correctly.
        with self.client:
            response = self.client.post(
                '/register',
                data=dict(
                    email='test@tester.com',
                    password='testing',
                    confirm='testing'
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'<h1>Welcome, <em>test@tester.com</em>!</h1>',
                response.data
            )
            self.assertTrue(current_user.email == 'test@tester.com')
            self.assertTrue(current_user.is_authenticated())
            self.assertTrue(current_user.is_active())
            self.assertFalse(current_user.is_anonymous())
            self.assertTrue(current_user.is_student())
            self.assertFalse(current_user.is_teacher())
            self.assertFalse(current_user.is_admin())
            self.assertEqual(response.status_code, 200)

    def test_student_registration_unique_email(self):
        # Ensure a student cannot register with a duplicate email.
        with self.client:
            response = self.client.post(
                '/register',
                data=dict(
                    email='student@student.com',
                    password='student',
                    confirm='student'
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'Sorry. That email is already taken.',
                response.data
            )
            self.assertTemplateUsed('user/register.html')
            self.assertEqual(response.status_code, 200)

    def test_update_password(self):
        # Ensure update password behaves correctly.
        with self.client:
            self.client.post(
                '/login',
                data=dict(
                    email='student@student.com',
                    password='student_user',
                ),
                follow_redirects=True
            )
            self.client.post(
                '/password',
                data=dict(
                    password='updated_student_password',
                    confirm='updated_student_password'
                ),
                follow_redirects=True
            )
            self.client.get('/logout', follow_redirects=True)
            response = self.client.post(
                '/login',
                data=dict(
                    email='student@student.com',
                    password='updated_student_password',
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'<h1>Welcome, <em>student@student.com</em>!</h1>',
                response.data
            )
            self.assertTrue(current_user.email == 'student@student.com')
            self.assertTrue(current_user.is_authenticated())
            self.assertTrue(current_user.is_active())
            self.assertFalse(current_user.is_anonymous())
            self.assertTrue(current_user.is_student())
            self.assertFalse(current_user.is_teacher())
            self.assertFalse(current_user.is_admin())
            self.assertEqual(response.status_code, 200)

    def test_update_password2(self):
        # Ensure update password behaves correctly.
        with self.client:
            self.client.post(
                '/login',
                data=dict(
                    email='student@student.com',
                    password='student_user',
                ),
                follow_redirects=True
            )
            response = self.client.post(
                '/password',
                data=dict(
                    password='short',
                    confirm='short'
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'<h1>Update Password</h1>',
                response.data
            )
            self.assertIn(
                b'Field must be between 6 and 25 characters long.',
                response.data
            )
            self.assertTrue(current_user.email == 'student@student.com')
            self.assertTrue(current_user.is_authenticated())
            self.assertTrue(current_user.is_active())
            self.assertFalse(current_user.is_anonymous())
            self.assertTrue(current_user.is_student())
            self.assertFalse(current_user.is_teacher())
            self.assertFalse(current_user.is_admin())
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
