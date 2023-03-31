from rest_framework import serializers
from rest_framework.response import Response
from user_auth.models import ServiceProvider
from user_auth.models import User_data


class ServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields = "__all__"

class UserRegistrationSerializer(serializers.ModelSerializer):
    # We are writing this becoz we need confirm password field in our Registratin Request
    # password2 = serializers.CharField(
    #     style={'input_type': 'password'}, write_only=True)

    # service_provider = ServiceProviderSerializer(many=True)

    class Meta:
        model = User_data 
        fields = ['email', 'first_name', 'last_name', 'contact_no','address','password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        # password2 = attrs.get('password2')
        # if password != password2:
        #     raise serializers.ValidationError(
        #         "Password and Confirm Password doesn't match")
        return attrs

    def create(self, validate_data):
        return User_data.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User_data
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User_data
        fields = "__all__" #['email', 'first_name', 'last_name','description', 'role', 'contact_no']


from django.contrib.auth.password_validation import validate_password

class ChangePasswordSerializer(serializers.Serializer):
    model = User_data

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
  

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User_data
        fields = ['token']