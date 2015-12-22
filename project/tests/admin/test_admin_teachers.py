# project/tests/admin/test_admin_teachers.py


import unittest

from project.tests.base import BaseTestCaseAdmin


class TestAdminBlueprintTeachers(BaseTestCaseAdmin):

    def test_admin_add_teacher_page(self):
        # Ensure an admin can view add teacher page.
        with self.client:
            response = self.client.get('/admin/add_teacher')
            self.assertIn(
                b'<h1>Add Teacher</h1>',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_admin_add_teacher(self):
        # Ensure an admin can add a new teacher.
        with self.client:
            response = self.client.post(
                '/admin/add_teacher',
                data=dict(
                    email='good@teacher.com',
                    password='bad_teacher',
                    confirm='bad_teacher'
                ),
                follow_redirects=True
            )
            self.assertIn(b'<h1>Dashboard</h1>', response.data)
            self.assertIn(b'<h2>Courses', response.data)
            self.assertIn(b'<table class="table">', response.data)
            self.assertIn(b'<th scope="row">1</th>', response.data)
            self.assertIn(b'<p>No courses!</p>', response.data)
            self.assertIn(b'<h2>Teachers', response.data)
            self.assertIn(b'<td>teacher@teacher.com</td>', response.data)
            self.assertIn(b'<td>good@teacher.com</td>', response.data)
            self.assertEqual(response.status_code, 200)

    def test_admin_add_teacher_unique_email(self):
        # Ensure an admin cannot add a new teacher with a duplicate email.
        with self.client:
            response = self.client.post(
                '/admin/add_teacher',
                data=dict(
                    email='teacher@teacher.com',
                    password='teacher_user',
                    confirm='teacher_user'
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'Sorry. That email is already taken.',
                response.data
            )
            self.assertTemplateUsed('/admin/add_teacher.html')
            self.assertEqual(response.status_code, 200)

    def test_admin_edit_teacher_page(self):
        # Ensure a admin can view edit teacher page.
        with self.client:
            response = self.client.get('/admin/update_teacher/2')
            self.assertIn(
                b'<h1>Update Teacher</h1>',
                response.data
            )
            self.assertIn(
                b'<input class="form-control" id="email" name="email" \
required type="text" value="teacher@teacher.com">',
                response.data
            )
            self.assertIn(
                b'<input class="form-control" id="registered_on" \
name="registered_on" required type="date" value="',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_admin_edit_teacher(self):
        # Ensure a admin can edit an individual teacher.
        with self.client:
            self.client.get('/admin/update_teacher/2')
            response = self.client.post(
                '/admin/update_teacher/2',
                data=dict(
                    email='update@teacher.com',
                    registered_on='2005-05-26',
                ),
                follow_redirects=True
            )
            self.assertIn(b'<h1>Dashboard</h1>', response.data)
            self.assertIn(b'<table class="table">', response.data)
            self.assertIn(b'<th scope="row">1</th>', response.data)
            self.assertIn(b'<h2>Teachers', response.data)
            self.assertIn(b'<td>update@teacher.com</td>', response.data)
            self.assertIn(b'<td>2005-05-26</td>', response.data)
            self.assertNotIn(b'<td>teacher@teacher.com</td>', response.data)
            self.assertEqual(response.status_code, 200)

    def test_admin_delete_teacher(self):
        # Ensure a admin can delete an individual teacher.
        with self.client:
            self.client.delete('/admin/teacher/3')
            self.client.delete('/admin/teacher/2')
            response = self.client.get('/admin/dashboard/')
            self.assertIn(b'<h1>Dashboard</h1>', response.data)
            self.assertIn(b'<p>No teachers!</p>', response.data)
            self.assertNotIn(b'teacher@teacher.com', response.data)
            self.assertNotIn(b'michael@teacher.com', response.data)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
