# tests/test_admin.py


import unittest

from flask.ext.login import current_user

from base import BaseTestCase


class TestAdminBlueprint(BaseTestCase):

    def test_admin_login(self):
        # Ensure login behaves correctly.
        with self.client:
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
                b'<li><a href="/admin/">Dashboard</a></li>',
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


if __name__ == '__main__':
    unittest.main()
