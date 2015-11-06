# tests/test_student.py


import datetime
import unittest

from flask.ext.login import current_user

from base import BaseTestCase
from project import bcrypt
from project.models import User
from project.user.forms import LoginForm


class TestStudentBlueprint(BaseTestCase):

    def test_student_registration(self):
        # Ensure registration behaves correctly.
        with self.client:
            response = self.client.post(
                '/register',
                data=dict(
                    email="student@student.com",
                    password="student",
                    confirm="student"
                ),
                follow_redirects=True
            )
            self.assertIn(b'Hi', response.data)
            self.assertIn(
                b'<li><a href="/students/">Dashboard</a></li>',
                response.data
            )
            self.assertTrue(current_user.email == "student@student.com")
            self.assertTrue(current_user.is_authenticated())
            self.assertTrue(current_user.is_active())
            self.assertFalse(current_user.is_anonymous())
            self.assertTrue(current_user.is_student())
            self.assertFalse(current_user.is_teacher())
            self.assertFalse(current_user.is_admin())
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
