from rest_framework import serializers
from scilicium_django_react.ontologies.models import Topics,Keyword, ExperimentalProcess, Granularity, Sequencing, Omics, Species, Organ, Tissue, CellLine, DevStage, Pathology, Chemical, BiomaterialType


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

class BiomaterialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiomaterialType
        fields = "__all__"

class DevStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevStage
        fields = "__all__"

class OrganSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organ
        fields = "__all__"

class PathologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pathology
        fields = "__all__"

class ChemicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chemical
        fields = "__all__"

class OmicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Omics
        fields = "__all__"

class SequencingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sequencing
        fields = "__all__"

class GranularitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Granularity
        fields = "__all__"

class ExperimentalProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentalProcess
        fields = "__all__"

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = "__all__"

class TopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = "__all__"
