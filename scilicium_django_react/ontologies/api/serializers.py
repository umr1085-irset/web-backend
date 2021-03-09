from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from scilicium_django_react.ontologies.models import Species, Cell, CellLine, Tissue, DevStage


class TissueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tissue
        fields = (
            "id",
            "name"
        )

class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = (
            "id",
            "name"
        )

class CellLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CellLine
        fields = (
            "id",
            "name"
        )

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = (
            "id",
            "name"
        )

class DevStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevStage
        fields = (
            "id",
            "name"
        )