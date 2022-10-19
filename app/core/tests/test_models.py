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
        self.assertEqual(user.check_password(password), True)
    
    def test_new_user_email_normalised(self):
        sample_emails = [
            ['test1@Example.com', 'test1@example.com'],
            ['Test@exAmple.com', 'Test@example.com'],
            ['Test@exAmple.COM', 'Test@example.com']

        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'kasdfj')
            self.assertEqual(user.email, expected)