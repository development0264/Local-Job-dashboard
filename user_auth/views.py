
from django.contrib.sites.shortcuts import get_current_site
from urllib import response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view 
from .utils import *
from user_auth.serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from user_auth.renderers import UserRenderer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import EmailMessage
from django.urls import reverse
import jwt

from django.core.mail import send_mail
from django.conf import settings
from API.settings import SECRET_KEY

import random
import string


class UserRegistrationView(APIView):

    serializer_class = UserRegistrationSerializer

    def post(self, request):
        user =  request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        user_data = serializer.data
        user = User_data.objects.get(email=user_data['email'])

        token = str(RefreshToken.for_user(user).access_token)
        user.access_token = token
        user.save()

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')

        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits , k=30))
        index = random.randint(0, len(random_string))

        absurl = f'http://{current_site}{relativeLink}?hS23D={random_string[:index]}&tA={user.id}&l2xS={random_string[index:]}'
        email_body = f'Hi {user.first_name}, use the link below to verify your email:\n{absurl}'
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email', 'user_id': user.id}
        Util.send_email(data)

        return Response({'token': token, 'msg': 'Registration successful', 'absurl': absurl}, status=status.HTTP_201_CREATED)

class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer
    def get(self, request):
        token = request.GET.get('tA')
        user = User_data.objects.get(id= token)
        user.is_verified = True
        user.save()
        return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)



@method_decorator(csrf_exempt, name='dispatch')
class UserLogin(APIView):
    def post(self, request, format = None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password =serializer.data.get('password')
            user = authenticate(email=email, password=password)            
            if user is not None and user.is_verified:
                token = str(RefreshToken.for_user(user).access_token)
                return Response({'token': token , 'msg' : 'Login Successfull'}, status=status.HTTP_200_OK)
            if user is None:
                return Response ({'errors': {'non_field_errors':['Email or password is not valid']}},
                status=status.HTTP_404_NOT_FOUND)
            else:
                return Response ({'errors': 'user is not verified'},
                status=status.HTTP_404_NOT_FOUND)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import generics
import re
def has_password_chars(password):
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$'
    return bool(re.match(pattern, password))
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User_data
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
            if len(serializer.data.get("new_password"))<=8:
                print("=======================.............",serializer.data.get("new_password"))
                print("=======================......type...",type(serializer.data.get("new_password")))
                return Response({"new_password": "password at least have 8 characters"}, status=status.HTTP_400_BAD_REQUEST)
            if has_password_chars(serializer.data.get("new_password")) == False:
                return Response({"new_password": "password must have at least one uppercase letter, \n at least one lowercase letter, \n at least least one digit, \n at least one special character"}, status=status.HTTP_400_BAD_REQUEST)
            if serializer.data.get("new_password") != serializer.data.get("confirm_password"):
                return Response({"msg": "password not match"}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def service_provider(request):
    
    if request.user.is_authenticated and request.user.is_verified:
        if (request.method == 'POST'):
            service_provider = ServiceProvider.objects.all()
            print(service_provider)
            serializers = ServiceProviderSerializer(data=request.data)
            serializers.is_valid()
            user = serializers.validated_data.get('user')
            work_field =serializers.validated_data.get('work_field')
            
            if ServiceProvider.objects.filter(user=user, work_field=work_field).exists():
                    return Response({'msg': 'user is already register for this service'}, status=status.HTTP_201_CREATED)   
                
            if serializers.is_valid():
                serializers.save()    
                return Response(serializers.data, status=status.HTTP_201_CREATED)            
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Authentication Error'}, status=status.HTTP_400_BAD_REQUEST)