# project/tests/admin/test_admin_dashboard.py


import unittest

from flask.ext.login import current_user

from project.tests.base import BaseTestCaseAdmin


class TestAdminBlueprintDashboard(BaseTestCaseAdmin):

    def test_admin_login(self):
        # Ensure login behaves correctly.
        with self.client:
            self.client.get('/logout')
            response = self.client.post(
                '/login',
                data=dict(
                    email='admin@admin.com',
                    password='admin_user',
                    confirm='admin_user'
                ),
                follow_redirects=True
            )
            self.assertIn(b'Welcome, <em>admin@admin.com</em>!', response.data)
            self.assertIn(
                b'<li><a href="/admin/dashboard/">Dashboard</a></li>',
                response.data
            )
            self.assertIn(
                b'<li><a href="/password">Update Password</a></li>',
                response.data
            )
            self.assertTrue(current_user.email == "admin@admin.com")
            self.assertTrue(current_user.is_authenticated)
            self.assertTrue(current_user.is_active)
            self.assertFalse(current_user.is_anonymous())
            self.assertFalse(current_user.is_student())
            self.assertFalse(current_user.is_teacher())
            self.assertTrue(current_user.is_admin())
            self.assertEqual(response.status_code, 200)

    def test_validate_admin_decorator(self):
        # Ensure a user has to be an admin to view the admin dashboard.
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
                '/admin/dashboard',
                follow_redirects=True
            )
            self.assertIn(
                b'You do not have the correct permissions to view that page.',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_admin_dashboard(self):
        # Ensure an admin can view the admin dashboard.
        with self.client:
            response = self.client.get(
                '/admin/dashboard',
                follow_redirects=True
            )
            self.assertIn(b'<h1>Dashboard</h1>', response.data)
            self.assertIn(b'<p>No courses!</p>', response.data)
            self.assertIn(b'<h2>Students', response.data)
            self.assertIn(b'<table class="table">', response.data)
            self.assertIn(b'<th scope="row">1</th>', response.data)
            self.assertIn(b'<td>student@student.com</td>', response.data)
            self.assertIn(b'<h2>Teachers', response.data)
            self.assertIn(b'<td>teacher@teacher.com</td>', response.data)
            self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_with_courses(self):
        # Ensure an admin can view courses on the admin dashboard.
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
            response = self.client.get(
                '/admin/dashboard',
                follow_redirects=True
            )
            self.assertIn(b'<h1>Dashboard</h1>', response.data)
            self.assertIn(b'<h2>Courses', response.data)
            self.assertIn(b'<table class="table">', response.data)
            self.assertIn(b'<th scope="row">1</th>', response.data)
            self.assertIn(b'<td>Music Appreciation</td>', response.data)
            self.assertIn(b'<td>teacher@teacher.com</td>', response.data)
            self.assertIn(b'<td>True</td>', response.data)
            self.assertNotIn(b'<p>No courses!</p>', response.data)
            self.assertIn(b'<h2>Students', response.data)
            self.assertIn(b'<td>student@student.com</td>', response.data)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
