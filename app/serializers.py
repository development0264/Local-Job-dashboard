from rest_framework import serializers
from .models import *
from user_auth.models import *

class JobSerializers(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"

class UserFeedbackSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = "__all__"

class BidForJobSerializers(serializers.ModelSerializer):
    class Meta:
        model = BidForJob
        fields = "__all__"

class PaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = BidForJob
        fields = ["job_completed"]
