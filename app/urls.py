from django.urls import path
from .views import *


urlpatterns = [
     path('api/job', Job_list, name="job"),
     path('api/job/<int:pk>', Job_details,name="job_details"),
     path('api/user_feedback', user_feedback,name="user_feedback"),
     path('api/bids', bids_list,name="bids_list"),
     path('api/bids/<int:pk>', bids,name="bids"),
     path('api/payment/<int:pk>', payment,name="payment"),

     # path('api/create', CreateQRView.as_view(), name="songs-list-create"),
]
