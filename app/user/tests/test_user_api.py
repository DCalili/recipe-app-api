"""
Tests for the user API.
"""
from django.test import TestCase
from django.auth.contrib import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import stats


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model.objects().create_user(**params);


class PublicUserApiTests(TestCase):
    """Test the pulic features of the user API."""
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.stats_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists"""
        payload = {
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if assword less than 5 chars."""
        payload = {
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
                email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
