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
                    email='stu@dent.com',
                    password='student_user',
                    confirm='student_user'
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'Welcome, <em>stu@dent.com</em>!',
                response.data
            )
            self.assertIn(
                b'<li><a href="/student/courses">View Courses</a></li>',
                response.data
            )
            self.assertTrue(current_user.email == "stu@dent.com")
            self.assertTrue(current_user.is_authenticated)
            self.assertTrue(current_user.is_active)
            self.assertFalse(current_user.is_anonymous())
            self.assertTrue(current_user.is_student())
            self.assertFalse(current_user.is_teacher())
            self.assertFalse(current_user.is_admin())
            self.assertEqual(response.status_code, 200)

    def test_student_login(self):
        # Ensure login behaves correctly.
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(
                    email='student@student.com',
                    password='student_user',
                    confirm='student_user'
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'Welcome, <em>student@student.com</em>!',
                response.data
            )
            self.assertIn(
                b'<li><a href="/student/courses">View Courses</a></li>',
                response.data
            )
            self.assertTrue(current_user.email == "student@student.com")
            self.assertTrue(current_user.is_authenticated)
            self.assertTrue(current_user.is_active)
            self.assertFalse(current_user.is_anonymous())
            self.assertTrue(current_user.is_student())
            self.assertFalse(current_user.is_teacher())
            self.assertFalse(current_user.is_admin())
            self.assertEqual(response.status_code, 200)

    def test_student_courses(self):
        # Ensure a student can view all courses s/he are taking.
        with self.client:
            self.client.post(
                '/login',
                data=dict(
                    email='student@student.com',
                    password='student_user',
                    confirm='student_user'
                ),
                follow_redirects=True
            )
            response = self.client.get('/student/courses')
            self.assertIn(
                b'<h1>All Courses</h1>',
                response.data
            )
            self.assertIn(
                b'<p>You are not taking any courses.</p>',
                response.data
            )
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main
