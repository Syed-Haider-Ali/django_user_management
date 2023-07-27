from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password

from user_auth.models import User
from utils.custom_exceptions import PasswordMustBeEightChar


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class VerifyOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(
        label=_("otp"),
        style={"input_type": "otp"},
        trim_whitespace=False,
        write_only=True
    )

    new_password = serializers.CharField(
        label=_("new_password"),
        style={"input_type": "new_password"},
        trim_whitespace=False,
        write_only=True
    )
    
    confirm_password = serializers.CharField(
        label=_("confirm_password"),
        style={"input_type": "confirm_password"},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, instance):
        user = self.context.get("user")
        if len(instance["new_password"]) < 6:
            raise PasswordMustBeEightChar()
        return instance

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("email"),
        write_only=True
    )


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(
        label=_("username"),
        
        write_only=True
    )
    password = serializers.CharField(
        label=_("password"),
        style={"input_type": "password"},
        # trim_whitespace=False,
        write_only=True
    )
    def validate(self, instance):
        if len(instance["password"]) < 4:
            raise serializers.ValidationError(_("Password must be at least 8 characters long."))
        if User.objects.filter(username=instance["username"], is_active=False, is_locked=True).exists():
            raise serializers.ValidationError(_("Your account has been deactivated."))
        return instance