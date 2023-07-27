from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from utils.base_authentication import JWTAuthentication
from user_auth.user_controller import RegisterController,LogoutController, LoginController, UserListController, ForgetPasswordController, VerifyOtpController


register_controller = RegisterController()
login_controller = LoginController()
logout_controller = LogoutController()
user_list_controller = UserListController()
forget_password_controller = ForgetPasswordController()
verify_otp_controller = VerifyOtpController()



class VerifyOtpAPIView(ModelViewSet):
    def post(self,request):
        return verify_otp_controller.verify_otp(request)

class ForgetPasswordAPIView(ModelViewSet):
    def post(self,request):
        return forget_password_controller.forget_password(request)

class RegisterAPIView(ModelViewSet):
    def create(self,request):
        return register_controller.create(request)

class LoginAPIView(ModelViewSet):
    def login(self,request):
        return login_controller.login(request)
    
class LogoutAPIView(ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    def logout(self,request):
        return logout_controller.logout(request)
    
class UserListAPIView(ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,IsAdminUser)
    def get(self,request):
        return user_list_controller.user_list(request)
    
    
