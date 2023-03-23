
from django.contrib.sites.shortcuts import get_current_site
from urllib import response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
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
        print("============",user.email)
        mail=user.email
        user.access_token = token
        user.save()

        print("===============",request.user)
        print("=================>User",user.id)

        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')


        absurl = 'http://'+str(current_site)+relativeLink+"?token="+str(user.id)
        email_body = 'Hi '+user.first_name + ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,'email_subject': 'Verify your email','user_id':user.id}
        Util.send_email(data)
        return Response ({'token': token, 'msg': 'Registration Successfull'}, status=status.HTTP_201_CREATED)

class VerifyEmail(APIView):
    
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        uemail = request.GET.get('email')
        print("========================>Email",token)
        
        user = User_data.objects.get(id= token)
        user.is_verified = True
        user.save()

        print("==================",token)
        return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)



@method_decorator(csrf_exempt, name='dispatch')
class UserLogin(APIView):
    def post(self, request, format = None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password =serializer.data.get('password')
            user = authenticate(email=email, password=password)            
            if user is not None:
                work_field = user.work_field
                token = str(RefreshToken.for_user(user).access_token)
                return Response({'token': token , 'msg' : 'Login Successfull','work_field':work_field}, status=status.HTTP_200_OK)
            else:
                return Response ({'errors': {'non_field_errors':['Email or password is not valid']}},
                status=status.HTTP_404_NOT_FOUND)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format = None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import generics
class ChangePasswordView(generics.UpdateAPIView):
    queryset = User_data.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

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

