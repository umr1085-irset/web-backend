from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from scilicium_django_react.datasets.models import Dataset, Loom, sopMeta, biomaterialMeta
from scilicium_django_react.ontologies.api.serializers import *
from scilicium_django_react.utils.loom_reader import *
from scilicium_django_react.studies.models import *

class biomaterialMetaSerializer(serializers.ModelSerializer):
    tissue = TissueSerializer(many=True, read_only=True)
    species = SpeciesSerializer(many=True, read_only=True)
    cell_line = CellLineSerializer(many=True, read_only=True)
    organ = OrganSerializer(many=True, read_only=True)
    dev_stage = DevStageSerializer(many=True, read_only=True)
    
    class Meta:
        model = biomaterialMeta
        fields = "__all__"

class sopMetaSerializer(serializers.ModelSerializer):
    omics= TissueSerializer(many=True, read_only=True)
    technoGrain = GranularitySerializer(many=True, read_only=True)
    technology = OmicsSerializer(many=True, read_only=True)
    expProcess = ExperimentalProcessSerializer(many=True, read_only=True)
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

class PublicDatasetSerializer(serializers.ModelSerializer):
    loom = LoomSerializer(many=False, read_only=True)
    technology = serializers.SerializerMethodField('getTechnologies')
    type = serializers.SerializerMethodField('getType')
    gender = serializers.SerializerMethodField('getGender')
    devStage = serializers.SerializerMethodField('getDevStage')
    tissue = serializers.SerializerMethodField('getTissues')

    def getTechnologies(self, dataset):
        return dataset.sop.technology.ontologyLabel
    
    def getType(self, dataset):
        return dataset.sop.omics.ontologyLabel

    def getGender(self, dataset):
        return dataset.bioMeta.gender

    def getTissues(self, dataset):
        tissues = list()
        for tissue in dataset.bioMeta.tissue.all() :
            tissues.append(tissue.ontologyLabel) if tissue.ontologyLabel not in tissues else tissues
        return tissues
    
    def getDevStage(self, dataset):
        devStage = list()
        for stage in dataset.bioMeta.dev_stage.all() :
            devStage.append(stage.ontologyLabel) if stage.ontologyLabel not in devStage else devStage
        return devStage

    class Meta:
        model = Dataset
        fields = "__all__"

        lookup_field = 'datasetId'
        extra_kwargs = {
            'url': {'lookup_field': 'datasetId'}
        }

class DatasetSerializer(serializers.ModelSerializer):
    loom = LoomSerializer(many=False, read_only=True)
    sop = sopMetaSerializer(many=False, read_only=True)
    bioMeta = biomaterialMetaSerializer(many=False, read_only=True)
    metadata = serializers.SerializerMethodField('get_metadata')
    rel_datasets = serializers.SerializerMethodField('get_relativedatasets')
    reductions = serializers.SerializerMethodField('get_reduction')
    default_display = serializers.SerializerMethodField('get_default_display')
    
    def get_reduction(self, dataset):
        reductions = dataset.loom.reductions
        return reductions
    
    def get_default_display(self, dataset):
        if dataset.loom.default_display :
            return dataset.loom.default_display
        else :
            return dataset.loom.reductions[0]
            
    def get_metadata(self, dataset):
        metadata = {'col_name':'','row_name':'','filters':{},'filters_keys':{'ca':[],'ra':[]}}
        for col in dataset.loom.classes :
           metadata['filters'][col] = {'name':col,'values':get_ca(dataset.loom.file.path,key=col,unique=True),'attributes':'ca'}
           metadata['filters_keys']['ca'].append(col)

        #Always add Chromosome on row attributes
        metadata['filters']['Chromosome'] = {'name':'Chromosome','values':get_ra(dataset.loom.file.path,key='Chromosome',unique=True),'attributes':'ra'}
        metadata['filters_keys']['ra'].append('Chromosome')
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
