"""
Tests for the user API.
"""

import django
from django.urls import reverse
from faker import Faker
from rest_framework import status

from core.test_setup import TestSetup, generate_user
from user.models import User

fake = Faker()


class TestsUserApi(TestSetup):
    """
    Test User API views.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super(TestsUserApi, cls).setUpClass()
        django.setup()

    def setUp(self) -> None:
        """Set up test case."""
        self.url = reverse("user:user_list")

        return super().setUp()

    def test_get_user_list(self):
        """Test get user list."""
        User.objects.all().delete()
        users = generate_user(quantity=3)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["id"], users[0].id)
        self.assertEqual(response.data[1]["id"], users[1].id)
        self.assertEqual(response.data[2]["id"], users[2].id)
        self.assertEqual(response.data[0]["email"], users[0].email)
        self.assertEqual(response.data[1]["email"], users[1].email)
        self.assertEqual(response.data[2]["email"], users[2].email)
        self.assertEqual(response.data[0]["first_name"], users[0].first_name)
        self.assertEqual(response.data[1]["first_name"], users[1].first_name)
        self.assertEqual(response.data[2]["first_name"], users[2].first_name)
        self.assertEqual(response.data[0]["last_name"], users[0].last_name)
        self.assertEqual(response.data[1]["last_name"], users[1].last_name)
        self.assertEqual(response.data[2]["last_name"], users[2].last_name)
        self.assertEqual(response.data[0]["document"], users[0].document)
        self.assertEqual(response.data[1]["document"], users[1].document)
        self.assertEqual(response.data[2]["document"], users[2].document)
        self.assertEqual(response.data[0]["phone_number"], users[0].phone_number)
        self.assertEqual(response.data[1]["phone_number"], users[1].phone_number)
        self.assertEqual(response.data[2]["phone_number"], users[2].phone_number)
        self.assertEqual(response.data[0]["is_active"], users[0].is_active)
        self.assertEqual(response.data[1]["is_active"], users[1].is_active)
        self.assertEqual(response.data[2]["is_active"], users[2].is_active)

    def test_empty_user_list(self):
        """Test get empty user list."""
        User.objects.all().delete()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.data, [])
