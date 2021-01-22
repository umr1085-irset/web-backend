from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from scilicium_django_react.datasets.models import Dataset, Data


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = "__all__"

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = "__all__"