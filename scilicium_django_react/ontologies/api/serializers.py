from rest_framework import serializers
from scilicium_django_react.ontologies.models import Species, CellLine, Tissue, DevStage


class TissueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tissue
        fields = "__all__"

class CellLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CellLine
        fields = "__all__"

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = "__all__"

class DevStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevStage
        fields = "__all__"