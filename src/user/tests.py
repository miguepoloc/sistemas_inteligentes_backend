"""
Tests for the user API.
"""

from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User

fake = Faker()


class TestsUserApi(TestCase):
    def setUp(self) -> None:
        self.url_user = reverse('user:user')
        self.payload = {
            "email": fake.email(),
            "username": fake.user_name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "document": fake.random_number(digits=10),
            "code_phone": "+57",
            "phone_number": fake.random_number(digits=10),
            "city": fake.city(),
            "password": fake.password(),
        }
        self.client = APIClient()

    # def test_create_user(self):
    #     """Test creating a new user."""
    #     res = self.client.post(self.url_user, self.payload)

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data["message"], "User created successfully")
    #     self.assertNotIn("password", res.data)

    #     users = User.objects.all()
    #     self.assertEqual(users.count(), 1)

    #     user = users.filter(email=self.payload["email"]).first()
    #     self.assertTrue(user.check_password(self.payload["password"]))
    #     self.assertEqual(user.email, self.payload["email"])
    #     self.assertEqual(user.username, self.payload["username"])
    #     self.assertEqual(user.first_name, self.payload["first_name"])
    #     self.assertEqual(user.last_name, self.payload["last_name"])
    #     self.assertEqual(user.document, self.payload["document"])
    #     self.assertEqual(user.code_phone, self.payload["code_phone"])
    #     self.assertEqual(user.phone_number, self.payload["phone_number"])
    #     self.assertEqual(user.city, self.payload["city"])
    #     self.assertFalse(user.is_admin)
    #     self.assertFalse(user.is_superuser)
    #     self.assertTrue(user.is_active)

    def test_create_user_without_email(self):
        """Test creating a new user without email."""
        payload = self.payload.copy()
        payload.pop("email")
        res = self.client.post(self.url_user, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["email"][0], "This field is required.")

    def test_error_create_user_with_email_existing(self):
        """Test error creating a new user with email existing."""
        User.objects.create_user(**self.payload)

        res = self.client.post(self.url_user, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["message"], "Error creating user, email already exists")

    def test_error_create_user_with_phone_number_existing(self):
        """Test error creating a new user with phone number existing."""
        User.objects.create_user(**self.payload)

        self.payload["email"] = fake.email()
        res = self.client.post(self.url_user, self.payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["message"], "Error creating user, phone number already exists")

    # def test_create_user_without_username(self):
    #     """Test creating a new user without username."""
    #     payload = self.payload.copy()
    #     payload.pop("username")
    #     res = self.client.post(self.url_user, payload)

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(res.data["message"], "User created successfully")

    # def test_update_user(self):
    #     """Test updating an existing user."""
    #     user = User.objects.create_user(**self.payload)

    #     payload = {
    #         "username": fake.user_name(),
    #         "first_name": fake.first_name(),
    #         "last_name": fake.last_name(),
    #         "document": fake.random_number(digits=10),
    #         "code_phone": "+57",
    #         "phone_number": fake.random_number(digits=10),
    #         "city": fake.city(),
    #     }
    #     self.client.force_authenticate(user=user)
    #     res = self.client.put(self.url_user, payload)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data["message"], "User updated successfully")

    #     user.refresh_from_db()
    #     self.assertEqual(user.username, payload["username"])
    #     self.assertEqual(user.first_name, payload["first_name"])
    #     self.assertEqual(user.last_name, payload["last_name"])
    #     self.assertEqual(user.document, payload["document"])
    #     self.assertEqual(user.code_phone, payload["code_phone"])
    #     self.assertEqual(user.phone_number, payload["phone_number"])
    #     self.assertEqual(user.city, payload["city"])

    def test_error_user_id(self):
        """Test error user id."""
        user = User.objects.create_user(**self.payload)
        payload = {
            "id": 100,
            "username": fake.user_name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "document": fake.random_number(digits=10),
            "code_phone": "+57",
            "phone_number": fake.random_number(digits=10),
            "city": fake.city(),
        }
        self.client.force_authenticate(user=user)
        res = self.client.put(self.url_user, payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.data["message"], f"User with id {payload['id']} not found")

    def test_error_put_without_id(self):
        """Test error put without id."""
        payload = {
            "username": fake.user_name(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "document": fake.random_number(digits=10),
            "code_phone": "+57",
            "phone_number": fake.random_number(digits=10),
            "city": fake.city(),
        }
        res = self.client.put(self.url_user, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["message"], "User id not found")

    def test_error_email_existing(self):
        """Test error email existing."""
        user = User.objects.create_user(**self.payload)
        payload = {
            "id": user.id,
            "email": self.payload["email"],
        }
        self.client.force_authenticate(user=user)
        res = self.client.put(self.url_user, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["message"], "Error updating user, email already exists")

    def test_error_phone_number_existing(self):
        """Test error phone number existing."""
        user = User.objects.create_user(**self.payload)
        payload = {
            "id": user.id,
            "phone_number": self.payload["phone_number"],
            "code_phone": self.payload["code_phone"],
        }
        self.client.force_authenticate(user=user)
        res = self.client.put(self.url_user, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["message"], "Error updating user, phone number already exists")
