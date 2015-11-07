# tests/test_student.py


import unittest

from flask.ext.login import current_user

from base import BaseTestCase


class TestStudentBlueprint(BaseTestCase):

    def test_student_registration(self):
        # Ensure registration behaves correctly.
        with self.client:
            response = self.client.post(
                '/register',
                data=dict(
                    email='stu@sdent.com',
                    password='student_user',
                    confirm='student_user'
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'Welcome, <em>stu@sdent.com</em>!',
                response.data
            )
            self.assertIn(
                b'<li><a href="/students/">Dashboard</a></li>',
                response.data
            )
            self.assertTrue(current_user.email == "stu@sdent.com")
            self.assertTrue(current_user.is_authenticated)
            self.assertTrue(current_user.is_active)
            self.assertFalse(current_user.is_anonymous())
            self.assertTrue(current_user.is_student())
            self.assertFalse(current_user.is_teacher())
            self.assertFalse(current_user.is_admin())
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main
