from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from scilicium_django_react.datasets.models import Dataset, Study


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = "__all__"

class StudyHudeCaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Study
        fields = "__all__"