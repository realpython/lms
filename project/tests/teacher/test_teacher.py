# project/tests/teacher/test_teacher.py


import unittest

from flask.ext.login import current_user

from project.tests.base import BaseTestCaseTeacher


class TestTeacherBlueprint(BaseTestCaseTeacher):

    def test_teacher_login(self):
        # Ensure login behaves correctly.
        with self.client:
            self.client.get('/logout')
            response = self.client.post(
                '/login',
                data=dict(
                    email='teacher@teacher.com',
                    password='teacher_user',
                    confirm='teacher_user'
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'Welcome, <em>teacher@teacher.com</em>!',
                response.data
            )
            self.assertIn(
                b'<li><a href="/teacher/courses">View Courses</a></li>',
                response.data
            )
            self.assertIn(
                b'<li><a href="/password">Update Password</a></li>',
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

    def test_teacher_courses(self):
        # Ensure a teacher can view all courses.
        with self.client:
            response = self.client.get('/teacher/courses')
            self.assertIn(
                b'<h1>All Courses</h1>',
                response.data
            )
            self.assertIn(
                b'<p>You are not teaching any courses.</p>',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_validate_teacher_decorator(self):
        # Ensure a user has to be a teacher to view all courses.
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
            response = self.client.get(
                '/teacher/courses',
                follow_redirects=True
            )
            self.assertIn(
                b'You do not have the correct permissions to view that page.',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_teacher_add_course_page(self):
        # Ensure a teacher can view add course page.
        with self.client:
            response = self.client.get('/teacher/add_course')
            self.assertIn(
                b'<h1>Add Course</h1>',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_teacher_add_course(self):
        # Ensure a teacher can add a new course.
        with self.client:
            response = self.client.post(
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
            self.assertIn(
                b'<h1>All Courses</h1>',
                response.data
            )
            self.assertIn(b'Music Appreciation', response.data)
            self.assertNotIn(
                b'<p>You are not teaching any courses.</p>',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_teacher_add_course_unique_name(self):
        # Ensure a teacher cannot add a new course with a duplicate name.
        with self.client:
            self.client.post(
                '/teacher/add_course',
                data=dict(
                    name='Chemistry',
                    subject='Science',
                    description='Get chemical',
                    start_date='2015-11-28',
                    end_date='2016-11-28',
                    teachers='teacher@teacher.com',
                    students=['student@student.com']
                ),
                follow_redirects=True
            )
            response = self.client.post(
                '/teacher/add_course',
                data=dict(
                    name='Chemistry',
                    subject='Science',
                    description='Get chemical',
                    start_date='2015-11-28',
                    end_date='2016-11-28',
                    teachers='teacher@teacher.com',
                    students=['student@student.com']
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'Sorry. That course name is already taken.',
                response.data
            )
            self.assertTemplateUsed('/teacher/add.html')
            self.assertEqual(response.status_code, 200)

    def test_teacher_view_courses(self):
        # Ensure a teacher can only view courses that they create.
        with self.client:
            self.client.post(
                '/teacher/add_course',
                data=dict(
                    name='Music Appreciation',
                    description='This course teaches you how to understand \
                                 what you are hearing.',
                    start_date='2015-11-06',
                    end_date='2015-11-07'
                ),
                follow_redirects=True
            )
            self.client.get('/logout')
            self.client.post(
                '/login',
                data=dict(
                    email='michael@teacher.com',
                    password='teacher_user',
                    confirm='teacher_user'
                ),
                follow_redirects=True
            )
            response = self.client.get('/teacher/courses')
            self.assertIn(
                b'<h1>All Courses</h1>',
                response.data
            )
            self.assertNotIn(b'<h1>Music Appreciation</h1>', response.data)
            self.assertIn(
                b'<p>You are not teaching any courses.</p>',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_teacher_view_course(self):
        # Ensure a teacher can view an individual course.
        with self.client:
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
            response = self.client.get('/teacher/course/1')
            self.assertIn(b'<h1>Music Appreciation</h1>', response.data)
            self.assertIn(
                b'This course teaches you how to understand',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_teacher_edit_course(self):
        # Ensure a teacher can edit an individual course.
        with self.client:
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
            response = self.client.post(
                '/teacher/update_course/1',
                data=dict(
                    name='Art Appreciation',
                    subject='Liberal Arts',
                    description='From here to there.',
                    start_date='2015-11-06',
                    end_date='2015-11-07'
                ),
                follow_redirects=True
            )
            self.assertIn(b'<h1>Art Appreciation</h1>', response.data)
            self.assertIn(b'From here to there.', response.data)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
