from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class RegisterAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('register')



ddq
    def test_create_user(self):
        new_user_data = {
            'first_name': 'Ali',
            'email': 's.haider0303@gmail.com',
            'username': 's.haider0303@gmail.com',
            'password': 'qwertyuiop123',
        }
        response = self.client.post(self.url, new_user_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)

    def test_register_without_email(self):
        user_data_with_blank_email = {
            'first_name': 'Ali',
            'email': '',
            'username': 's.haider0303@gmail.com',
            'password': 'qwertyuiop123',
        }
        user_data_with_no_email = {
            'first_name': 'Ali',
            'username': 's.haider0303@gmail.com',
            'password': 'qwertyuiop123',
        }
        response_blank_email = self.client.post(self.url, user_data_with_blank_email, format='json')
        response_no_email = self.client.post(self.url, user_data_with_no_email, format='json')
        self.assertEqual(response_blank_email.status_code, 400)
        self.assertEqual(response_no_email.status_code, 400)

    def test_register_without_username(self):
        user_data_with_blank_username = {
            'first_name': 'Ali',
            'email': 's.haider0303@gmail.com',
            'username': '',
            'password': 'qwertyuiop123',
        }
        user_data_with_no_username = {
            'first_name': 'Ali',
            'email': 's.haider0303@gmail.com',
            'password': 'qwertyuiop123',
        }
        response_with_blank_username = self.client.post(self.url, user_data_with_blank_username, format='json')
        response_with_no_username = self.client.post(self.url, user_data_with_no_username, format='json')
        self.assertEqual(response_with_blank_username.status_code, 400)
        self.assertEqual(response_with_no_username.status_code, 400)

    def test_register_without_password(self):
        user_data_with_password_less_than_7 = {
            'first_name': 'Ali',
            'username': 's.haider0303@gmail.com',
            'email': 's.haider0303@gmail.com',
            'password': 'abcd',
        }
        user_data_with_blank_password = {
            'first_name': 'Ali',
            'username': 's.haider0303@gmail.com',
            'email': 's.haider0303@gmail.com',
            'password': '',
        }
        user_data_with_no_password = {
            'first_name': 'Ali',
            'username': 's.haider0303@gmail.com',
            'email': 's.haider0303@gmail.com',
        }
        response_with_blank_password = self.client.post(self.url, user_data_with_blank_password, format='json')
        response_with_no_password = self.client.post(self.url, user_data_with_no_password, format='json')
        response_with_password_less_than_7 = self.client.post(self.url, user_data_with_password_less_than_7, format='json')
        self.assertEqual(response_with_blank_password.status_code, 400)
        self.assertEqual(response_with_no_password.status_code, 400)
        self.assertEqual(response_with_password_less_than_7.status_code, 400)

