# project/tests/admin/test_admin_students.py


import unittest

from project.tests.base import BaseTestCaseAdmin


class TestAdminBlueprintStudents(BaseTestCaseAdmin):

    def test_admin_add_student_page(self):
        # Ensure an admin can view add student page.
        with self.client:
            response = self.client.get('/admin/add_student')
            self.assertIn(
                b'<h1>Add Student</h1>',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_admin_add_student(self):
        # Ensure an admin can add a new student.
        with self.client:
            response = self.client.post(
                '/admin/add_student',
                data=dict(
                    email='good@student.com',
                    password='bad_student',
                    confirm='bad_student'
                ),
                follow_redirects=True
            )
            self.assertIn(b'<h1>Dashboard</h1>', response.data)
            self.assertIn(b'<h2>Courses', response.data)
            self.assertIn(b'<table class="table">', response.data)
            self.assertIn(b'<th scope="row">1</th>', response.data)
            self.assertIn(b'<p>No courses!</p>', response.data)
            self.assertIn(b'<h2>Students', response.data)
            self.assertIn(b'<td>student@student.com</td>', response.data)
            self.assertIn(b'<td>good@student.com</td>', response.data)
            self.assertEqual(response.status_code, 200)

    def test_admin_add_student_unique_email(self):
        # Ensure an admin cannot add a new student with a duplicate email.
        with self.client:
            response = self.client.post(
                '/admin/add_student',
                data=dict(
                    email='student@student.com',
                    password='student_user',
                    confirm='student_user'
                ),
                follow_redirects=True
            )
            self.assertIn(
                b'Sorry. That email is already taken.',
                response.data
            )
            self.assertTemplateUsed('/admin/add_student.html')
            self.assertEqual(response.status_code, 200)

    def test_admin_edit_student_page(self):
        # Ensure a admin can view edit student page.
        with self.client:
            response = self.client.get('/admin/update_student/1')
            self.assertIn(
                b'<h1>Update Student</h1>',
                response.data
            )
            self.assertIn(
                b'<input class="form-control" id="email" name="email" \
required type="text" value="student@student.com">',
                response.data
            )
            self.assertIn(
                b'<input class="form-control" id="registered_on" \
name="registered_on" required type="date" value="',
                response.data
            )
            self.assertEqual(response.status_code, 200)

    def test_admin_edit_student(self):
        # Ensure a admin can edit an individual student.
        with self.client:
            self.client.get('/admin/update_student/1')
            response = self.client.post(
                '/admin/update_student/1',
                data=dict(
                    email='update@student.com',
                    registered_on='2005-05-26',
                ),
                follow_redirects=True
            )
            self.assertIn(b'<h1>Dashboard</h1>', response.data)
            self.assertIn(b'<table class="table">', response.data)
            self.assertIn(b'<th scope="row">1</th>', response.data)
            self.assertIn(b'<h2>Students', response.data)
            self.assertIn(b'<td>update@student.com</td>', response.data)
            self.assertIn(b'<td>2005-05-26</td>', response.data)
            self.assertNotIn(b'<td>student@student.com</td>', response.data)
            self.assertEqual(response.status_code, 200)

    def test_admin_delete_student(self):
        # Ensure a admin can delete an individual student.
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
                '/teacher/add_student',
                data=dict(
                    email='delete@student.com',
                    password='delete_student',
                    confirm='delete_student'
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
            self.client.delete('/admin/student/1')
            response = self.client.get('/admin/dashboard/')
            self.assertIn(b'<h1>Dashboard</h1>', response.data)
            self.assertIn(b'<p>No students!</p>', response.data)
            self.assertNotIn(b'<td>delete@student.com</td>', response.data)
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
