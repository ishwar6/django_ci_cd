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
            ['Test2@exAmple.com', 'Test2@example.com'],
            ['Test3@exAmple.COM', 'Test3@example.com']

        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'kasdfj')
            self.assertEqual(user.email, expected)
    
    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)