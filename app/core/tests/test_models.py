"""
Test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """test creating a user with an email is successful"""
        email = 'test@example.com'
        password = '1234'
        user = get_user_model().objects.create_user(
            email = email, 
            password = password
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.check_password(password))