from rest_framework import serializers
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
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    token_user_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User_data
        fields = ('token_user_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_token_user_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"token_user_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
    

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User_data
        fields = ['token']