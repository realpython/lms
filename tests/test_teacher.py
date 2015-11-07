# tests/test_student.py


import unittest

from flask.ext.login import current_user

from base import BaseTestCase


class TestTeacherBlueprint(BaseTestCase):

    def test_teacher_login(self):
        # Ensure registration behaves correctly.
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(
                    email="teacher@teacher.com",
                    password="teacher",
                    confirm="teacher"
                ),
                follow_redirects=True
            )
            self.assertIn(b'Welcome!', response.data)
            self.assertIn(
                b'<li><a href="/teachers/">Dashboard</a></li>',
                response.data
            )
            self.assertTrue(current_user.email == "teacher@teacher.com")
            self.assertTrue(current_user.is_authenticated)
            self.assertTrue(current_user.is_active)
            self.assertFalse(current_user.is_anonymous())
            self.assertFalse(current_user.is_student())
            self.assertTrue(current_user.is_teacher())
            self.assertFalse(current_user.is_admin())
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
