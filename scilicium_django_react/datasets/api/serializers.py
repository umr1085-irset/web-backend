from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from scilicium_django_react.datasets.models import Dataset, Loom, sopMeta, biomaterialMeta
from scilicium_django_react.ontologies.api.serializers import *
from scilicium_django_react.utils.loom_reader import *
from scilicium_django_react.studies.models import *

class biomaterialMetaSerializer(serializers.ModelSerializer):
    tissue = TissueSerializer(many=True, read_only=True)
    species = SpeciesSerializer(many=True, read_only=True)
    organ = OrganSerializer(many=True, read_only=True)
    developmentStage = DevStageSerializer(many=True, read_only=True)
    
    class Meta:
        model = biomaterialMeta
        fields = "__all__"

class sopMetaSerializer(serializers.ModelSerializer):
    omics= OmicsSerializer(many=True, read_only=True)
    technoGrain = GranularitySerializer(many=True, read_only=True)
    technology = SequencingSerializer(many=True, read_only=True)
    molecules = ChemicalSerializer(many=True, read_only=True)
    expProcess = ExperimentalProcessSerializer(many=True, read_only=True)
    class Meta:
        model = sopMeta
        fields = "__all__"

class LoomSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, allow_null=True)
    class Meta:
        model = Loom
        fields = "__all__"



class LoomBasicSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False, allow_null=True)
    class Meta:
        model = Loom
        fields = ["file","cellNumber","geneNumber","loomId","id","col_name","row_name"]




class DatasetUnrelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loom
        fields = "__all__"

class PublicDatasetSerializer(serializers.ModelSerializer):
    loom = LoomSerializer(many=False, read_only=True)
    #sop = sopMetaSerializer(many=False, read_only=True)
    #bioMeta = biomaterialMetaSerializer(many=False, read_only=True)
    omics = serializers.SerializerMethodField('getOmics')
    resolution = serializers.SerializerMethodField('getGranularity')
    technology = serializers.SerializerMethodField('getTechnology')
    #technology = SequencingSerializer(many=True, read_only=True)
    #molecules = ChemicalSerializer(many=True, read_only=True)

    molecules  = serializers.SerializerMethodField('getMolecules')
    #expProcess = ExperimentalProcessSerializer(many=True, read_only=True)
    expProcess = serializers.SerializerMethodField('getExpProcess')
    techno_description = serializers.SerializerMethodField('getTechnoDescription')
    ageRange = serializers.SerializerMethodField('getAgeRange')
    developmentStage = serializers.SerializerMethodField('getDevStage')
    sex = serializers.SerializerMethodField('getSex')
    species = serializers.SerializerMethodField('getSpecies')
    organ = serializers.SerializerMethodField('getOrgans')
    tissue = serializers.SerializerMethodField('getTissues')
    diseaseStage = serializers.SerializerMethodField('getDiseaseStage')
    loomColInfo = serializers.SerializerMethodField('getLoomColInfo')


    #gender = serializers.SerializerMethodField('getGender')
    #devStage = serializers.SerializerMethodField('getDevStage')
    #tissue = serializers.SerializerMethodField('getTissues')

    
    def getLoomColInfo(self, dataset):
        unit = dataset.loom.col_name
        if unit is None : 
            unit = "cells"
        nb = str(dataset.loom.cellNumber)
        colInfo = nb + " " + unit
        return colInfo

    def getAgeRange(self, dataset):
        age_start = str(dataset.bioMeta.age_start)
        age_end = str(dataset.bioMeta.age_end)
        age_unit = dataset.bioMeta.age_unit
        ageRange = age_start + "-" + age_end + " " + age_unit
        return ageRange

    def getSex(self, dataset):
        return dataset.bioMeta.sex

    def getDiseaseStage(self, dataset):
        return dataset.bioMeta.diseaseStage

    def getSpecies(self, dataset):
        labels=[]
        for x in dataset.bioMeta.species.all():
            label = x.displayLabel;
            if label not in labels : 
                labels.append(label)
        return labels


    def getDevStage(self, dataset):
        labels=[]
        for x in dataset.bioMeta.developmentStage.all():
            label = x.displayLabel;
            if label not in labels : 
                labels.append(label)
        return labels

    def getOrgans(self, dataset):
        labels=[]
        for x in dataset.bioMeta.organ.all():
            label = x.displayLabel;
            if label not in labels : 
                labels.append(label)
        return labels

    def getTissues(self, dataset):
        labels=[]
        for x in dataset.bioMeta.tissue.all():
            label = x.displayLabel;
            if label not in labels : 
                labels.append(label)
        return labels


    def getOmics(self, dataset):
        labels=[]
        for x in dataset.sop.omics.all():
            label = x.displayLabel;
            if label not in labels : 
                labels.append(label)
        return labels

    
    
    def getGranularity(self, dataset):
        labels=[]
        for x in dataset.sop.resolution.all():
            label = x.displayLabel;
            if label not in labels : 
                labels.append(label)
        return labels 
    
    
    def getTechnology(self, dataset):
        labels=[]
        for x in dataset.sop.technology.all():
            label = x.displayLabel;
            if label not in labels : 
                labels.append(label)
        return labels 
    
    
    
    def getMolecules(self, dataset):
        labels=[]
        for x in dataset.sop.molecule_applied.all():
            label = x.displayLabel;
            if label not in labels : 
                labels.append(label)
        return labels 


    def getExpProcess(self, dataset):
        labels=[]
        for x in dataset.sop.experimentalDesign.all():
            label = x.displayLabel;
            if label not in labels : 
                labels.append(label)
        return labels 

    def getTechnoDescription(self, dataset):
        return dataset.sop.techno_description

    class Meta:
        model = Dataset
        fields = "__all__"

        lookup_field = 'datasetId'
        extra_kwargs = {
            'url': {'lookup_field': 'datasetId'}
        }



class BasicDatasetSerializer(serializers.ModelSerializer):
    loom = LoomSerializer(many=False, read_only=True)
    sop = sopMetaSerializer(many=False, read_only=True)
    bioMeta = biomaterialMetaSerializer(many=False, read_only=True)
    
    class Meta:
        model = Dataset
        fields = "__all__"

        lookup_field = 'datasetId'
        extra_kwargs = {
            'url': {'lookup_field': 'datasetId'}
        }


                                                                                                                                                                                                                                                                                                                                                                                       
class DatasetSerializer(serializers.ModelSerializer):
    loom = LoomBasicSerializer(many=False, read_only=True)
    #sop = sopMetaSerializer(many=False, read_only=True)
    #bioMeta = biomaterialMetaSerializer(many=False, read_only=True)
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
        #if len(dataset.loom.classes) > 6 : 
           # columns = dataset.loom.classes[0:6]
        #else :
            #columns = dataset.loom.classes
    
        metadata = get_ca_metalist(dataset.loom.file.path,metadata)
    
        #for col in columns :
           #metadata['filters'][col] = {'name':col,'values':get_ca(dataset.loom.file.path,key=col,unique=True),'attributes':'ca'}
           #metadata['filters_keys']['ca'].append(col)

        #Always add Chromosome on row attributes
        #if check_ra(dataset.loom.file.path,'Chromosome'):
            #metadata['filters']['Chromosome'] = {'name':'Chromosome','values':get_ra(dataset.loom.file.path,key='Chromosome',unique=True),'attributes':'ra'}
            #metadata['filters_keys']['ra'].append('Chromosome')
        #if check_ra(dataset.loom.file.path,'Symbol'):
            #metadata['filters']['Symbol'] = {'name':'Symbol','values':get_ra(dataset.loom.file.path,key='Symbol',unique=True),'attributes':'ra'}
            #metadata['filters_keys']['ra'].append('Symbol')
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
        fields = ["id","datasetId","title","description","loom","metadata","rel_datasets","reductions","default_display", "status"]


