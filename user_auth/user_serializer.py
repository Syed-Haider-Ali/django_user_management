from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from user_auth.models import User
from utils.custom_exceptions import PasswordMustBeEightChar, SameOldPassword, PasswordsDoesNotMatch, WrongOldPassword

class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(
        label=_("old_password"),
        style={"input_type": "old_password"},
        trim_whitespace=True,
        write_only=True
    )
    new_password = serializers.CharField(
        label=_("new_password"),
        style={"input_type": "new_password"},
        trim_whitespace=True,
        write_only=True
    )
    confirm_password = serializers.CharField(
        label=_("confirm_password"),
        style={"input_type": "confirm_password"},
        trim_whitespace=True,
        write_only=True
    )
    def validate(self, instance):
        user = self.context.get("user")
        if user.check_password(instance["old_password"]):
            if len(instance["new_password"]) < 8:
                raise PasswordMustBeEightChar()
            if instance["new_password"] == instance["old_password"]:
                raise SameOldPassword()
            if instance['new_password'] != instance['confirm_password']:
                raise PasswordsDoesNotMatch()
            return instance
        else:
            raise WrongOldPassword()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'



class VerifyOtpSerializer(serializers.Serializer):
    otp = serializers.CharField(
        label=_("otp"),
        style={"input_type": "otp"},
        trim_whitespace=True,
        write_only=True
    )
    new_password = serializers.CharField(
        label=_("new_password"),
        style={"input_type": "new_password"},
        trim_whitespace=True,
        write_only=True
    )
    confirm_password = serializers.CharField(
        label=_("confirm_password"),
        style={"input_type": "confirm_password"},
        trim_whitespace=True,
        write_only=True
    )
    def validate(self, instance):
        user = self.context.get("user")
        if user.check_password(instance["new_password"]):
            raise SameOldPassword()
        if len(instance["new_password"]) < 8:
            raise PasswordMustBeEightChar()
        if instance['new_password'] != instance['confirm_password']:
            raise PasswordsDoesNotMatch()
        return instance


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("email"),
        trim_whitespace=True,
        write_only=True
    )


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(
        label=_("username"),
        trim_whitespace=True,
        write_only=True
    )
    password = serializers.CharField(
        label=_("password"),
        style={"input_type": "password"},
        trim_whitespace = True,
        write_only=True
    )
    def validate(self, instance):
        if len(instance["password"]) < 4:
            raise serializers.ValidationError(_("Password must be at least 8 characters long."))
        if User.objects.filter(username=instance["username"], is_active=False, is_locked=True).exists():
            raise serializers.ValidationError(_("Your account has been deactivated."))
        return instance