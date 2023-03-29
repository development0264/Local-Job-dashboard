from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view , authentication_classes, permission_classes
import jwt
from django.conf import settings
from user_auth.views import UserRegistrationView
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class CustomPagination(PageNumberPagination):
    page_size = 5


# @permission_required([IsAuthenticated])
# @permission_required(permission_classes)
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAuthenticated])

@api_view(['GET', 'POST'])
def Job_list(request):
    if request.user.is_admin:
        if request.method == 'GET':
            paginator = CustomPagination()
            job = Job.objects.all()
            paginated_queryset = paginator.paginate_queryset(job, request)
            serializers = JobSerializers(paginated_queryset, many=True)
            print("======================admin can see all>>>>>>>>>>>>>",request.user.email)
            return Response(serializers.data)
        
    if request.user.is_authenticated and request.user.is_verified:
        if request.method == 'GET':
            feedback=UserFeedback.objects.all()
            job = Job.objects.all()
            usermail  = request.user.email
            print("======================>>>>>>>>>>>>>",usermail)
            average_rating = 0
            total_feedback = 0
            
            for f in feedback:
                if f.service_provider.user.email == usermail:
                    total_feedback +=1
                    average_rating += f.ratings
                    if f.ratings == 0:
                        average_rating = 1
                        total_feedback = 1
                    print(f.ratings)
            if total_feedback == 0:
                return Response({'msg': 'user is not eligible to see jobs!!'})
            print("======================>>>>>>>>>>>>>",average_rating)
            average = average_rating/total_feedback
            print("======================>>>>>>>>>>>>>",average_rating,total_feedback,average)
            print("Average")
            print(type(average))
            print(average)
            joblist = []
            if average <= 2:
                for j in job:
                    if j.budget <= 2000:
                        print("==========job=============",j)
                        joblist.append(j)
            if average < 4 and average > 2:
                for j in job:
                    if j.budget <= 6000:
                        print("==========job=============",j)
                        joblist.append(j)
            if average <= 5 and average >= 4:
                for j in job:
                    if j.budget <= 10000:
                        print("==========job=============",j)
                        joblist.append(j)
            serializers = JobSerializers(joblist, many=True)
            return Response(serializers.data)
                    

    if request.user.is_admin:
        if (request.method == 'POST'):
            user  =  User_data.objects.all()
            print(user)
            # if user.is_admin :
            serializers = JobSerializers(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Authentication Error \n user must be an admin'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def Job_details(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user.is_authenticated and request.user.is_verified:
        if request.method == 'GET':
            print("======================>>>>>>>>>>>>>",request.user.email)
            serializers = JobSerializers(job)
            return Response(serializers.data)

    if request.user.is_admin:
        if request.method == 'PUT':
            serializers = JobSerializers(job, request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            job.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def user_feedback(request):
    if request.user.is_authenticated and request.user.is_verified:
        if request.method == 'GET':
            paginator = CustomPagination()
            feedback = UserFeedback.objects.all()
            paginated_queryset = paginator.paginate_queryset(feedback, request)
            serializers = UserFeedbackSerializers(paginated_queryset, many=True)
            # serializers = UserFeedbackSerializers(feedback, many=True)
            return Response(serializers.data)

        elif (request.method == 'POST'):
            serializers = UserFeedbackSerializers(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Authentication Error'}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'POST'])
def bids_list(request):
    if request.user.is_admin:
        if request.method == 'GET':
            paginator = CustomPagination()
            bid=BidForJob.objects.all().order_by('job_biding_price')
            paginated_queryset = paginator.paginate_queryset(bid, request)
            serializers = BidForJobSerializers(paginated_queryset, many=True)
            # serializers = BidForJobSerializers(bid, many=True)
            return Response(serializers.data)

    if request.user.is_authenticated and request.user.is_verified:
        if request.method == 'GET':
            bid=BidForJob.objects.all()
            job = Job.objects.all()
            serializers = BidForJobSerializers(bid, many=True)
            return Response(serializers.data)
        
        if (request.method == 'POST'):
            bid = BidForJob.objects.all()
            print(bid)
            serializers = BidForJobSerializers(data=request.data)
            serializers.is_valid()
            service_provider = serializers.validated_data.get('service_provider')
            job =serializers.validated_data.get('job')
            
            if BidForJob.objects.filter(service_provider=service_provider, job=job).exists():
                 return Response({'msg': 'already bid'}, status=status.HTTP_201_CREATED)   
              
            if serializers.is_valid():
                serializers.save()    
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Authentication Error'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def bids(request, pk):
    if request.user.is_authenticated and request.user.is_verified:
        try:
            bid = BidForJob.objects.get(pk=pk)
        except BidForJob.DoesNotExist:
            return Response({'msg': 'bid not found'},status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializers = BidForJobSerializers(bid)
            if serializers.data:
                return Response(serializers.data)

        elif request.method == 'PUT':
            serializers = BidForJobSerializers(bid, request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            bid.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT'])
def payment(request, pk):
    if request.user.is_authenticated and request.user.is_verified:
        try:
            bid = BidForJob.objects.get(pk=pk)
        except BidForJob.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializers = PaymentSerializers(bid)
            # if bid.job_completed == True:
            return Response(serializers.data)

        elif request.method == 'PUT':
            serializers = BidForJobSerializers(bid, request.data)
            if serializers.is_valid():
                serializers.save()
                if bid.job_completed == True:
                    return Response({'msg': 'Payment Done'})
                else:
                    return Response({'msg': 'Payment Pending'})

            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
