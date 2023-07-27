from django.urls import resolve,reverse
from django.test import TestCase, SimpleTestCase
# from user_auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from blog_project import settings
# from django.conf import settings
# from rest_framework.authtoken.models import Token

from user_auth.models import User, Token
from user_auth.views import RegisterAPIView, LoginAPIView, ChangePasswordAPIView, VerifyOtpAPIView, ForgetPasswordAPIView,ListAPIView



class ListAPIViewTest(APITestCase):
    list_url = reverse('get_users_list')
    client=APIClient()
    # def setUp(self):
    #     self.user = User.objects.create(email='abc@gmail.com',username='abc@gmail.com',password='abc9898')
    #     self.token = self.user.get_access_token()
    #     print(self.token)
    #     self.client = APIClient()
    #     # self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
    #     self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token)

    def test_get_users_with_authentication_returns_200(self):
        self.client.force_authenticate(user=User(is_staff=True))
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_if_user_anonymus_and_returns_403(self):
        self.client.force_authenticate(user=User(is_staff=False))
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_users_by_id_with_authentication_returns_404(self):
        self.client.force_authenticate(user=User(is_staff=True))
        response = self.client.get(self.list_url+'?id=1')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    

# class LoginAPIViewTest(APITestCase):
#     login_url = reverse('login')
#     def setUp(self):
#         User.objects.create(email='abc@gmail.com',username='abc@gmail.com',password='abc9898')
#     def test_login(self):
# #         # user = User.objects.create(email='abc@gmail.com',username='abc@gmail.com',password='abc9898')
# #         # user.save()
# #         # self.token = self.user.get_access_token()
# #         # print(self.token)
# #         # print(user.email)
#         login_credentials = {
#             'username':'abc@gmail.com',
#             'password':'abc9898'
#         }
#         _response = self.client.post(self.login_url, data=login_credentials, format='json')
#         # self.assertNotEqual(_response.status_code,status.HTTP_200_OK)
#         self.assertEqual(_response.status_code,status.HTTP_200_OK)



class RegisterAPIViewTest(APITestCase):
    register_url = reverse('register')
    login_url = reverse('login')

    def setUp(self):
        self._data = {
            'first_name':'Ali Hassan',
            'last_name':'Gillani',
            'email':'alihassan@gmail.com',
            'username':'alihassan@gmail.com',
            'phone':'03408260804',
            'password':'hassan92' 
            }

    def test_register(self):
        _response = self.client.post(self.register_url, data=self._data, format='json')
        # _data = _response.json()
        self.assertEqual(_response.status_code,status.HTTP_201_CREATED)
        self.assertNotEqual(_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(_response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(_response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'alihassan@gmail.com')




# class LoginAPIViewTest(APITestCase):
#     login_url = reverse('login')
#     def test_login(self):
#         # user = User.objects.create(email='abc@gmail.com',username='abc@gmail.com',password='abc9898')
#         # user.save()
#         # self.token = self.user.get_access_token()
#         # print(self.token)
#         # print(user.email)
#         login_credentials = {
#             'username':'abc@gmail.com',
#             'password':'abc9898'
#         }
#         _response = self.client.post(self.login_url, data=login_credentials, format='json')
#         self.assertNotEqual(_response.status_code,status.HTTP_200_OK)
#         self.assertEqual(_response.status_code,status.HTTP_400_BAD_REQUEST)


class UserAuthUrlsTest(SimpleTestCase):
    def test_Urls(self):
        register = reverse('register')
        login = reverse('login')
        forget_password = reverse('forget_password')
        verify_otp = reverse('verify_otp')
        change_password = reverse('change_password')
        get_users_list = reverse('get_users_list')
        # print(resolve(url).func.__name__)
        # print(RegisterAPIView.__name__)
        self.assertEquals(resolve(register).func.__name__, RegisterAPIView.__name__)
        self.assertEquals(resolve(login).func.__name__, LoginAPIView.__name__)
        self.assertEquals(resolve(forget_password).func.__name__, ForgetPasswordAPIView.__name__)
        self.assertEquals(resolve(verify_otp).func.__name__, VerifyOtpAPIView.__name__)
        self.assertEquals(resolve(change_password).func.__name__, ChangePasswordAPIView.__name__)
        self.assertEquals(resolve(get_users_list).func.__name__, ListAPIView.__name__)

        self.assertNotEquals(resolve(get_users_list).func.__name__, ChangePasswordAPIView.__name__)







# class UserAPIViewTests(APITestCase):
#     url = reverse('get_users_list')

#     def setUp(self):
        
#         self.user = User.objects.create(username='oppo@gmail.com',email='oppo@gmail.com',password='haider98',phone='03408260804',is_active=True)
        

#     def test_get_users(self):
#         pass        

    # customers_url = reverse("customer")

    # def setUp(self):
    #     self.user = User.objects.create_user(
    #         username='admin', password='admin')
    #     self.token = Token.objects.create(user=self.user)
    #     #self.client = APIClient()
    #     self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    # def test_get_customers_authenticated(self):
    #     response = self.client.get(self.customers_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)




# class SecondTestCase(TestCase):
#     fixtures = ['main.json']
    
    # def setUp(self):
    #     # Set up test database in memory
    #     settings.DATABASES["test"]["ENGINE"] = "django.db.backends.sqlite3"
    #     settings.DATABASES["test"]["test_lcl_backend"] = ":memory:"
        
    #     from django.core.management import call_command
    #     call_command("migrate")
        
        # # Create a Test User
        # self.user = User.objects.create(
        #     username="testuser",
        #     email="test@yopmail.com",
        #     password="test1234",
        # )

        # # Test if user data is saved in Model
        # self.assertEqual(self.user.email, "tes@yopmail.com")

    
    # def test_Register(self):
    #     _data = {
    #         'first_name':'Fouzia',
    #         'last_name':'Saeed',
    #         'email':'fouzia95@gmail.com',
    #         'phone':'03408260804',
    #         'password':'fouzia95' 
    #         }
        
    #     _response = self.client.post('/users/register', data=_data, format='json')
    #     _data = _response.json()
        
    #     self.assertEqual(_response.status_code,status.HTTP_201_CREATED)
    #     # status.HTTP_400_BAD_REQUEST
    #     # status.HTTP_201_CREATED



# from django.conf import settings
# from django.test import TestCase
# from user_management.models import User


# class DjangoClientWithDB(TestCase):
#     def setUp(self):
#         # Set up test database in memory
#         settings.DATABASES["test"]["ENGINE"] = "django.db.backends.sqlite3"
#         settings.DATABASES["test"]["test_blog_backend"] = ":memory:"

#         # Create the schema for the test database
#         from django.core.management import call_command

#         call_command("migrate")

#         # Create a Test User
#         self.user = User.objects.create_user(
#             username="testuser",
#             email="test@yopmail.com",
#             password="test1234",
#         )

#         # Test if user data is saved in Model
#         self.assertEqual(self.user.email, "test@yopmail.com")

#         # Login User to Create Access Token
#         response = self.client.post(
#             "/login",
#             {"email": "test@yopmail.com", "password": "test1234"},
#             content_type="application/json",
#         ).json()

#         # Grab Access Token
#         access_token = response.get("data").get("token")

#         # Verify and Assign token
#         self.assertFalse(len(access_token) < 5)
#         self.token = "Bearer " + access_token

#     def tearDown(self):
#         # Destroy the test database after each test
#         del settings.DATABASES["test"]["test_lcl_backend"]
