from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from scilicium_django_react.studies.models import *


class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        read_only_fields = (
            "id",
        )
        fields = (
            "id",
            "name",
        )

class AuthorSerializer(serializers.ModelSerializer):
    affiliation = AffiliationSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        read_only_fields = (
            "id",
            "affiliation"
        )
        fields = (
            "id",
            "fullName",
            "affiliation"
        )

class ArticleSerializer(serializers.ModelSerializer):
    author =  AuthorSerializer(many=True, read_only=True)
    class Meta:
        model = Article
        read_only_fields = (
            "id",
            "author"
        )
        fields = (
            "id",
            "title",
            "abstract",
            "journal",
            "volume",
            "releaseDate",
            "author",

        )

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        read_only_fields = (
            "id",
            "projectId",
            "created_at",
            "created_by",
        )
        fields = (
            "id",
            "projectId",
            "created_at",
            "created_by",
            "description",
            "status",
            "title",

        )

class StudySerializer(serializers.ModelSerializer):

    project = ProjectSerializer(many=False, read_only=True)
    article = ArticleSerializer(many=True, read_only=True)
    class Meta:
        model = Study
        read_only_fields = (
            "id",
            "studyId",
            "created_at",
            "created_by",
            "updated_at",
            "project",
            "article"
        )
        fields = (
            "id",
            "studyId",
            "created_at",
            "created_by",
            "updated_at",
            "description",
            "status",
            "title",
            "topics",
            "project",
            "article"

        )
        lookup_field = 'studyId'
        extra_kwargs = {
            'url': {'lookup_field': 'studyId'}
        }