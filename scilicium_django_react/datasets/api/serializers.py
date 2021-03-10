from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from scilicium_django_react.datasets.models import Dataset, Loom, sopMeta, biomaterialMeta
from scilicium_django_react.ontologies.api.serializers import TissueSerializer, CellSerializer, CellLineSerializer, SpeciesSerializer

class biomaterialMetaSerializer(serializers.ModelSerializer):
    tissue = TissueSerializer(many=True, read_only=True)
    species = SpeciesSerializer(many=True, read_only=True)
    cell = CellSerializer(many=True, read_only=True)
    cell_line = CellLineSerializer(many=True, read_only=True)
    
    class Meta:
        model = biomaterialMeta
        fields = "__all__"

class sopMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = sopMeta
        fields = "__all__"

class LoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loom
        fields = "__all__"

class DatasetSerializer(serializers.ModelSerializer):
    loom = LoomSerializer(many=True, read_only=True)
    sop = sopMetaSerializer(many=False, read_only=True)
    bioMeta = biomaterialMetaSerializer(many=False, read_only=True)

    class Meta:
        model = Dataset
        fields = "__all__"

        lookup_field = 'datasetId'
        extra_kwargs = {
            'url': {'lookup_field': 'datasetId'}
        }
