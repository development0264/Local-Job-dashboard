from django.shortcuts import render

from user_auth.serializers import *
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

@api_view(['GET', 'POST'])
def Job_list(request):
    if request.user.is_admin:
        if request.method == 'GET':
            paginator = CustomPagination()
            job = Job.objects.all()
            paginated_queryset = paginator.paginate_queryset(job, request)
            serializers = JobSerializers(paginated_queryset, many=True)
            return Response(serializers.data)
        
    if request.user.is_authenticated and request.user.is_verified:
        if request.method == 'GET':                    
            try:
                service_provider = ServiceProvider.objects.get(user=request.user)
            except ServiceProvider.DoesNotExist:
                return Response({'msg': 'user is not service Provider or Admin'})

            joblist = [j for j in Job.objects.all()
                    if j.budget <= 2000 and service_provider.ratings <= 2
                    or j.budget <= 6000 and 2 < service_provider.ratings < 4
                    or j.budget <= 10000 and service_provider.ratings >= 4]
            print("==========jobs=============", joblist)

            serializers = JobSerializers(joblist, many=True)
            return Response(serializers.data)
                    

    if request.user.is_admin:
        if (request.method == 'POST'):
            serializers = JobSerializers(data=request.data)         
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Authentication Error user must be an admin'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def Job_details(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response({'msg': 'job does not exist'},status=status.HTTP_404_NOT_FOUND)
    try:
        service_provider = ServiceProvider.objects.get(user=request.user)
    except ServiceProvider.DoesNotExist:
        return Response({'msg': 'user is not service Provider or Admin'})

    if request.user.is_authenticated and request.user.is_verified:
        if request.method == 'GET':                    
            if service_provider.ratings <= 2:
                max_budget = 2000
            elif service_provider.ratings < 4:
                max_budget = 6000
            else:
                max_budget = 10000

            if job.budget <= max_budget:
                serializers = JobSerializers(job)
                return Response(serializers.data)
            else:
                return Response({'msg': 'User is not eligible to see this job because of low ratings.'})

    if request.user.is_admin:
        if request.method == 'PUT':
            serializers = JobSerializers(job, request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            job.delete()
            return Response({'msg': 'job is deleted'},status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'Authentication Error user must be an admin'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def user_feedback(request):
    if request.user.is_authenticated and request.user.is_verified:
        if request.method == 'GET':
            paginator = CustomPagination()
            feedback = UserFeedback.objects.all()
            paginated_queryset = paginator.paginate_queryset(feedback, request)
            serializers = UserFeedbackSerializers(paginated_queryset, many=True)
            return Response(serializers.data)

        elif (request.method == 'POST'):
            serializers = UserFeedbackSerializers(data=request.data)
            
            
            if serializers.is_valid():
                current_user = serializers.validated_data.get('user')
                ratings = serializers.validated_data.get('ratings')
                service_provider =serializers.validated_data.get('service_provider')
                
                if current_user != request.user and not request.user.is_admin:
                    return Response({'msg': 'user is not current user!'}, status=status.HTTP_400_BAD_REQUEST)

                if UserFeedback.objects.filter(user=current_user, service_provider=service_provider).exists():
                    return Response({'msg': 'user has already gave feedback to this service provider'}, status=status.HTTP_400_BAD_REQUEST)
                sp = ServiceProvider.objects.get(id = service_provider.id)
                sp.ratings = (sp.ratings + ratings)/2
                sp.save()
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
            return Response(serializers.data)

    if request.user.is_authenticated and request.user.is_verified:
        if request.method == 'GET':
            bid=BidForJob.objects.all()
            serializers = BidForJobSerializers(bid, many=True)
            return Response(serializers.data)
        
        if (request.method == 'POST'):
            bid = BidForJob.objects.all()
            print(bid)
            serializers = BidForJobSerializers(data=request.data)
            serializers.is_valid()
            service_provider = serializers.validated_data.get('service_provider')
            job =serializers.validated_data.get('job')
            if service_provider.user.email != request.user.email and not request.user.is_admin:
                return Response({'msg': 'user who is biding is not current user or admin!!'},status=status.HTTP_400_BAD_REQUEST)     
            if BidForJob.objects.filter(service_provider=service_provider, job=job).exists():
                return Response({'msg': 'current user has already bid on this job'},  status=status.HTTP_400_BAD_REQUEST)   
              
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
            return Response({'msg': 'bid not found or does not exist'},status=status.HTTP_400_BAD_REQUEST)

        if bid.service_provider.user != request.user and not request.user.is_admin:
            return Response({'msg': 'user is not Current User or Admin'},status=status.HTTP_400_BAD_REQUEST)
            
        if request.method == 'GET':
            serializers = BidForJobSerializers(bid)
            return Response(serializers.data)

        elif request.method == 'PUT':
            serializers = BidForJobSerializers(bid, request.data)
            if serializers.is_valid():
                service_provider = serializers.validated_data.get('service_provider')
                job =serializers.validated_data.get('job')
                if BidForJob.objects.filter(service_provider=service_provider, job=job).exists():
                    return Response({'msg': 'already bid'}, status=status.HTTP_400_BAD_REQUEST)   
                serializers.save()
                return Response(serializers.data)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            bid.delete()
            return Response({'msg': 'bid is deleted'},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'PUT'])
def payment(request, pk):
    if request.user.is_authenticated and request.user.is_verified:
        try:
            bid = BidForJob.objects.get(pk=pk)
        except BidForJob.DoesNotExist:
            return Response({'msg': 'bid not found or doesn not exist'},status=status.HTTP_404_NOT_FOUND)

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
    
