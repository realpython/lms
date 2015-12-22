# project/tests/student/test_student.py


import unittest

from flask.ext.login import current_user

from project.tests.base import BaseTestCaseStudent


class TestStudentBlueprint(BaseTestCaseStudent):

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
            self.client.get('/logout', follow_redirects=True)
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
            self.assertIn(
                b'<li><a href="/password">Update Password</a></li>',
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

    def test_student_add_course_page_without_courses(self):
        # Ensure a student can view add course page with no available courses.
        with self.client:
            response = self.client.get('/student/add_course')
            self.assertIn(
                b'<h1>Add Course</h1>',
                response.data
            )
            self.assertIn(
                b'No new courses at this time.',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_student_add_course_page_with_courses(self):
        # Ensure a student can view add course page with available courses.
        with self.client:
            self.client.post(
                '/login',
                data=dict(
                    email='teacher@teacher.com',
                    password='teacher_user',
                    confirm='teacher_user'
                ),
                follow_redirects=True
            )
            self.client.post(
                '/teacher/add_course',
                data=dict(
                    name='Music Appreciation',
                    subject='Liberal Arts',
                    description='This course teaches you how to understand \
                                 what you are hearing.',
                    start_date='2015-11-06',
                    end_date='2015-11-07'
                ),
                follow_redirects=True
            )
            self.client.get('/logout', follow_redirects=True)
            self.client.post(
                '/login',
                data=dict(
                    email='student@student.com',
                    password='student_user',
                    confirm='student_user'
                ),
                follow_redirects=True
            )
            response = self.client.get('/student/add_course')
            self.assertIn(
                b'<h1>Add Course</h1>',
                response.data
            )
            self.assertIn(
                b'Music Appreciation',
                response.data
            )
            self.assertNotIn(
                b'No new courses at this time.',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_student_add_course(self):
        # Ensure a student can add a new course.
        with self.client:
            self.client.post(
                '/login',
                data=dict(
                    email='teacher@teacher.com',
                    password='teacher_user',
                    confirm='teacher_user'
                ),
                follow_redirects=True
            )
            self.client.post(
                '/teacher/add_course',
                data=dict(
                    name='Music Appreciation',
                    subject='Liberal Arts',
                    description='This course teaches you how to understand \
                                 what you are hearing.',
                    start_date='2015-11-06',
                    end_date='2015-11-07'
                ),
                follow_redirects=True
            )
            self.client.get('/logout', follow_redirects=True)
            self.client.post(
                '/login',
                data=dict(
                    email='student@student.com',
                    password='student_user',
                    confirm='student_user'
                ),
                follow_redirects=True
            )
            response = self.client.post(
                '/student/add_course',
                data=dict(courses='Music Appreciation'),
                follow_redirects=True
            )
            self.assertIn(
                b'Thank you for adding a new course.',
                response.data
            )
            self.assertIn(
                b'<h1>All Courses</h1>',
                response.data
            )
            self.assertIn(
                b'Music Appreciation',
                response.data
            )
            self.assertNotIn(
                b'<p>You are not taking any courses.</p>',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_student_view_course(self):
        # Ensure a student can view an individual course.
        with self.client:
            self.client.post(
                '/login',
                data=dict(
                    email='teacher@teacher.com',
                    password='teacher_user',
                    confirm='teacher_user'
                ),
                follow_redirects=True
            )
            self.client.post(
                '/teacher/add_course',
                data=dict(
                    name='Music Appreciation',
                    subject='Liberal Arts',
                    description='This course teaches you how to understand \
                                 what you are hearing.',
                    start_date='2015-11-06',
                    end_date='2015-11-07'
                ),
                follow_redirects=True
            )
            self.client.get('/logout', follow_redirects=True)
            self.client.post(
                '/login',
                data=dict(
                    email='student@student.com',
                    password='student_user',
                    confirm='student_user'
                ),
                follow_redirects=True
            )
            self.client.post(
                '/student/add_course',
                data=dict(courses='Music Appreciation'),
                follow_redirects=True
            )
            response = self.client.get('/student/course/1')
            self.assertIn(
                b'<h1>Music Appreciation</h1>',
                response.data
            )
            self.assertIn(
                b'This course teaches you how to understand',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_validate_student_decorator(self):
        # Ensure a user has to be a student to view all courses.
        with self.client:
            self.client.post(
                '/login',
                data=dict(
                    email='teacher@teacher.com',
                    password='teacher_user',
                    confirm='teacher_user'
                ),
                follow_redirects=True
            )
            response = self.client.get(
                '/student/courses',
                follow_redirects=True
            )
            self.assertIn(
                b'You do not have the correct permissions to view that page.',
                response.data
            )
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main
