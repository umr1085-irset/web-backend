from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from scilicium_django_react.projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        read_only_fields = (
            "id",
            "created_at",
            "created_by",
        )
        fields = (
            "id",
            "created_at",
            "created_by",
            "description",
            "status",
            "name",

        )