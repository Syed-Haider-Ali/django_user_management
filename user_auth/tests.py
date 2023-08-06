from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class RegisterAPITest(APITestCase):
    def setUp(self):
        # self.user_data = {
        #     'first_name': 'Ali',
        #     'email': 's.haider0303@gmail.com',
        #     'username': 's.haider0303@gmail.com',
        #     'password': 'qwertyuiop123',
        # }
        # self.user = User.objects.create(**self.user_data)
        self.url = reverse('register')

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

    def test_register_error_cases(self):
        new_user_data = {
            'first_name': 'Ali',

            'username': 's.haider0303@gmail.com',
            'password': 'qwertyuiop123',
        }
        response = self.client.post(self.url, new_user_data, format='json')
        self.assertEqual(response.status_code, 400)
