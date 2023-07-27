import threading
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from authentication.settings import EMAIL_HOST_USER
from user_auth.user_serializer import UserSerializer, LoginSerializer, ForgetPasswordSerializer, VerifyOtpSerializer
from user_auth.models import Token, User
from utils.reusable_methods import get_first_error_message, generate_six_length_random_number
from utils.response_messages import *
from utils.helper import create_response, paginate_data



class VerifyOtpController:
    serializer_class = VerifyOtpSerializer
    
    def verify_otp(self,request):
        request.POST._mutable = True
        request.data["new_password"] = request.data.get("new_password").strip()
        request.data["confirm_password"] = request.data.get("confirm_password").strip()
        new_password = make_password(request.data["new_password"])
        request.POST._mutable = False
        # check OTP time delay
        time_delay = timezone.now() - timezone.timedelta(seconds=300)
        user = User.objects.filter(otp=request.data.get("otp"), otp_generated_at__gt=time_delay).first()

        if not user:
            create_response({},INVALID_OTP, status_code=400)

        serialized_data = self.serializer_class(data=request.data, context={"user": user})

        if not serialized_data.is_valid():
            return create_response({},get_first_error_message(serialized_data.errors,UNSUCCESSFUL), status_code=400)

        if request.data.get('new_password') != request.data.get('confirm_password'):
            return create_response({}, PASSWORD_DOES_NOT_MATCH, status_code=400)
        
        user.password = new_password
        user.otp = None
        user.save()
        return create_response({},SUCCESSFUL, status_code=200)
        

class ForgetPasswordController:
    
    serializer_class = ForgetPasswordSerializer
    
    def forget_password(self,request):
        serialized_data = self.serializer_class(data=request.data)
        if not serialized_data.is_valid():
            create_response({},get_first_error_message(serialized_data.errors, UNSUCCESSFUL), status_code=400 )
        
        user = User.objects.filter(email=request.data['email']).first()
        if not user:
            create_response({}, USER_NOT_FOUND, status_code=404)

        otp = generate_six_length_random_number()
        user.otp = otp
        user.otp_generated_at = timezone.now()
        user.save()
        subject = "Password Recovery Request"
        message = f"""
            Hi {user.first_name} {user.last_name},
            Your request for password recovery has been received.
            Please use the following otp.
            OTP: {otp}
            """
        recipient_list = [request.data.get("email")]
        t = threading.Thread(target=send_mail, args=(subject, message, EMAIL_HOST_USER, recipient_list))
        t.start()
        return create_response({}, EMAIL_SUCCESSFULLY_SENT, status_code=200)


class RegisterController:
    serializer_class = UserSerializer

    def create(self,request):
        request.POST._mutable = True
        request.data['password'] = make_password(request.data['password'])
        request.POST._mutable = False
        
        serialized_data = self.serializer_class(data=request.data)

        if serialized_data.is_valid():
            instance = serialized_data.save()
            return create_response(self.serializer_class(instance).data, SUCCESSFUL, status_code=200)
        else:
            return create_response({}, get_first_error_message(serialized_data.errors, UNSUCCESSFUL), status_code=400)
        
        
class UserListController:
    serializer_class = UserSerializer
    
    # only superuser can access 
    def user_list(self,request):
        if request.user.is_superuser:
            data_from_model = self.serializer_class.Meta.model.objects.all()
            filtered_data = self.filterset_class(request.GET, queryset=data_from_model)
            data = filtered_data.qs
            
            if not data:   
                return create_response({}, 'You have no record', status_code=200)
            paginated_data = paginate_data(data, request)
            count = data.count()
            
            serialized_data = self.serializer_class(paginated_data, many=True).data
            response_data = {
                "count":count,
                "data":serialized_data,
            }
            return create_response(response_data, SUCCESSFUL, status_code=200)
        else:
            return create_response({}, NOT_A_SUPERUSER, status_code=400)


class LoginController:
    serializer_class = LoginSerializer

    def login(self, request):
        request.POST._mutable = True
        request.data["username"] = request.data.get("username", "").strip()
        request.data["password"] = request.data.get("password", "").strip()
        request.POST._mutable = False
        username = request.data['username']
        password = request.data['password']
        serialized_data = self.serializer_class(data=request.data)
        
        if not serialized_data.is_valid():
            return Response({'error':get_first_error_message(serialized_data.errors, UNSUCCESSFUL)}, status=400)
     
        user = authenticate( username=username, password=password)
        if not user:
            return create_response({}, message=INCORRECT_EMAIL_OR_PASSWORD, status_code=400)
        
        response_data = {
            "token": user.get_access_token(),
            "name": user.get_full_name(),
            "username":user.username,
        } 
        Token.objects.update_or_create(defaults={"token": response_data.get("token")},user_id=user.id)
        user.failed_login_attempts = 0
        user.last_failed_time = None
        user.last_login = timezone.now()
        user.save()
        return create_response(response_data, SUCCESSFUL, status_code=200)
        

class LogoutController:
    def logout(self,request):
        user = request.user.id
        token = Token.objects.filter(user=user)
        if not token:
            return create_response({},UNSUCCESSFUL, status_code=400)
        token.delete()
        return create_response({}, SUCCESSFUL, status_code=200)        
        
