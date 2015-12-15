# project/tests/admin/test_admin_courses.py


import unittest

from project.tests.base import BaseTestCase


class TestAdminBlueprintCourses(BaseTestCase):

    def test_admin_add_course_page(self):
        # Ensure an admin can view add course page.
        with self.client:
            self.client.post(
                '/login',
                data=dict(
                    email='admin@admin.com',
                    password='admin_user',
                    confirm='admin_user'
                ),
                follow_redirects=True
            )
            response = self.client.get('/admin/add_course')
            self.assertIn(
                b'<h1>Add Course</h1>',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_admin_add_course(self):
        # Ensure an admin can add a new course.
        with self.client:
            self.client.post(
                '/login',
                data=dict(
                    email='admin@admin.com',
                    password='admin_user',
                    confirm='admin_user'
                ),
                follow_redirects=True
            )
            response = self.client.post(
                '/admin/add_course',
                data=dict(
                    name='Chemistry',
                    subject='Science',
                    description='Get chemical',
                    start_date='2015-11-28',
                    end_date='2016-11-28',
                    teachers='teacher@teacher.com'
                ),
                follow_redirects=True
            )
            self.assertIn(b'<h1>Dashboard</h1>', response.data)
            self.assertIn(b'<h2>Courses', response.data)
            self.assertIn(b'<table class="table">', response.data)
            self.assertIn(b'<th scope="row">1</th>', response.data)
            self.assertIn(b'<td>Chemistry</td>', response.data)
            self.assertIn(b'Get chemical', response.data)
            self.assertIn(b'<td>teacher@teacher.com</td>', response.data)
            self.assertNotIn(b'<p>No courses!</p>', response.data)
            self.assertIn(b'<h2>Students', response.data)
            self.assertIn(b'<td>student@student.com</td>', response.data)
            self.assertEqual(response.status_code, 200)

    def test_admin_edit_course_page(self):
        # Ensure a admin can view edit course page.
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
            self.client.get('/logout')
            self.client.post(
                '/login',
                data=dict(
                    email='admin@admin.com',
                    password='admin_user',
                    confirm='admin_user'
                ),
                follow_redirects=True
            )
            response = self.client.get('/admin/update_course/1')
            self.assertIn(
                b'<h1>Update Course</h1>',
                response.data
            )
            self.assertIn(
                b'<input class="form-control" id="name" \
name="name" required type="text" value="Music Appreciation">',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_admin_edit_course(self):
        # Ensure a admin can edit an individual course.
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
            self.client.get('/logout')
            self.client.post(
                '/login',
                data=dict(
                    email='admin@admin.com',
                    password='admin_user',
                    confirm='admin_user'
                ),
                follow_redirects=True
            )
            self.client.get('/admin/update_course/1')
            response = self.client.post(
                '/admin/update_course/1',
                data=dict(
                    name='Art Appreciation',
                    subject='Liberal Arts',
                    description='From here to there.',
                    start_date='2015-11-06',
                    end_date='2015-11-07',
                    teachers='teacher@teacher.com'
                ),
                follow_redirects=True
            )
            self.assertIn(b'<h1>Dashboard</h1>', response.data)
            self.assertIn(b'<h2>Courses', response.data)
            self.assertIn(b'<table class="table">', response.data)
            self.assertIn(b'<th scope="row">1</th>', response.data)
            self.assertIn(b'<td>Art Appreciation</td>', response.data)
            self.assertIn(b'From here to there.', response.data)
            self.assertIn(b'<td>teacher@teacher.com</td>', response.data)
            self.assertIn(b'<h2>Students', response.data)
            self.assertIn(b'<td>student@student.com</td>', response.data)
            self.assertEqual(response.status_code, 200)

    def test_admin_delete_course(self):
        # Ensure a admin can delete an individual course.
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
            self.client.get('/logout')
            self.client.post(
                '/login',
                data=dict(
                    email='admin@admin.com',
                    password='admin_user',
                    confirm='admin_user'
                ),
                follow_redirects=True
            )
            self.client.delete('/admin/course/1')
            response = self.client.get('/admin/dashboard/')
            self.assertIn(b'<h1>Dashboard</h1>', response.data)
            self.assertIn(b'<p>No courses!</p>', response.data)
            self.assertNotIn(b'<td>Music Appreciation</td>', response.data)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
