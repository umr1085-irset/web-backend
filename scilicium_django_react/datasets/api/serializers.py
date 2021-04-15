from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from scilicium_django_react.datasets.models import Dataset, Loom, sopMeta, biomaterialMeta
from scilicium_django_react.ontologies.api.serializers import TissueSerializer, CellSerializer, CellLineSerializer, SpeciesSerializer
from scilicium_django_react.utils.loom_reader import *
from scilicium_django_react.studies.models import *

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

class DatasetUnrelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loom
        fields = "__all__"

class DatasetSerializer(serializers.ModelSerializer):
    loom = LoomSerializer(many=False, read_only=True)
    sop = sopMetaSerializer(many=False, read_only=True)
    bioMeta = biomaterialMetaSerializer(many=False, read_only=True)
    metadata = serializers.SerializerMethodField('get_metadata')
    rel_datasets = serializers.SerializerMethodField('get_relativedatasets')
    
    def get_metadata(self, dataset):
        metadata = {'col_name':'','row_name':'','filters':[],'filters_keys':[]}
        for col in dataset.loom.classes :
           metadata['filters'].append({'name':col,'values':get_ca(dataset.loom.file.path,key=col,unique=True),'attributes':'ca'})
           metadata['filters_keys'].append(col)

        #Always add Chromosome on row attributes
        metadata['filters'].append({'name':'Chromosome','values':get_ra(dataset.loom.file.path,key='Chromosome',unique=True),'attributes':'ra'})
        
        metadata['row_name'] = dataset.loom.row_name
        metadata['col_name'] = dataset.loom.col_name
        metadata['cell_number'] = dataset.loom.cellNumber
        metadata['gene_number'] = dataset.loom.geneNumber
        return metadata
    
    def get_relativedatasets(self, dataset):
        d_id_list = []
        all_datasets = list(dataset.study.dataset_of.all())
        for i in all_datasets :
            if i.datasetId != dataset.datasetId :
                loom = i.loom
                d_id_list.append({'id': i.datasetId, 'title':i.title, 'gene_number': loom.geneNumber, 'cell_number': loom.cellNumber, 'col_name': loom.col_name, 'row_name': loom.row_name})
        return {'datasets':d_id_list}

    class Meta:
        model = Dataset
        fields = "__all__"

        lookup_field = 'datasetId'
        extra_kwargs = {
            'url': {'lookup_field': 'datasetId'}
        }
