from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from scilicium_django_react.studies.models import *
from scilicium_django_react.datasets.api.serializers import DatasetSerializer, BasicDatasetSerializer
from scilicium_django_react.users.api.serializers import GetFullUserSerializer


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

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        read_only_fields = (
            "id",
        )
        fields = (
            "id",
            "name",
            "team",
        )

class ViewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viewer
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
            "pmid"

        )

class ProjectSerializer(serializers.ModelSerializer):
    created_by = GetFullUserSerializer(many=False, read_only=True)
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
        lookup_field = 'projectId'
        extra_kwargs = {
            'url': {'lookup_field': 'projectId'}
        }

class StudySerializer(serializers.ModelSerializer):

    collection = ProjectSerializer(many=False, read_only=True)
    article = ArticleSerializer(many=True, read_only=True)
    dataset_of = BasicDatasetSerializer(many=True, read_only=True)
    created_by = GetFullUserSerializer(many=False, read_only=True)
    contributor = ContributorSerializer(many=True, read_only=True)
    viewer = ViewerSerializer(many=True, read_only=True)
    class Meta:
        model = Study
        read_only_fields = (
            "id",
            "studyId",
            "created_at",
            "created_by",
            "updated_at",
            "project",
            "contributor",
            "article",
            "dataset_of",
            "viewer"
        )
        fields = "__all__"
        lookup_field = 'studyId'
        extra_kwargs = {
            'url': {'lookup_field': 'studyId'}
        }

class StudyPublicSerializer(serializers.ModelSerializer):

    authors = serializers.SerializerMethodField('get_authors')
    pub_date = serializers.SerializerMethodField('get_pub_date')
    technology = serializers.SerializerMethodField('get_technology')
    species = serializers.SerializerMethodField('get_species')
    dev_stage = serializers.SerializerMethodField('get_dev_stage')
    tissues = serializers.SerializerMethodField('get_tissues')
    organs = serializers.SerializerMethodField('get_organs')
    gender = serializers.SerializerMethodField('get_gender')
    pmids = serializers.SerializerMethodField('get_pub_pmids')
    created_by = GetFullUserSerializer(many=False, read_only=True)
    viewer = ViewerSerializer(many=True, read_only=True)
    nb_dataset = serializers.SerializerMethodField('get_nb_datasets')
    shorthand = serializers.SerializerMethodField('get_shorthand')
    biomaterialType = serializers.SerializerMethodField('get_biotype')
    experimentalDesign = serializers.SerializerMethodField('get_design')
    pathology = serializers.SerializerMethodField('get_pathology')
    #age_range = serializers.SerializerMethodField('get_age_range')

    #def get_age_range(self, study):
    #    ageRanges = []
    #    for dataset in study.dataset_of.all():
    #        ageStart = dataset.bioMeta.age_start
    #        ageEnd = dataset.bioMeta.age_end
    #        ageUnit = dataset.bioMeta.age_unit
    #        ageRange = ageStart
    #        if ageRange not in ageRanges:
    #            ageRanges.append(ageRange)
    #    return ageRanges


    def get_nb_datasets(self, study): 
        nb = 0
        info = "1 dataset"
        for dataset in study.dataset_of.all():
            nb = nb + 1
        if nb > 1 : 
            info = str(nb) + " datasets"
        else :
            info = str(nb) + " dataset"
        return info
        

    def get_design(self,study):
        designs = []
        for dataset in study.dataset_of.all():
            for x in dataset.sop.experimentalDesign.all():
                if x.displayLabel not in designs:
                    designs.append(x.displayLabel)
        return designs

    def get_technology(self, study):
        technology = []
        for dataset in study.dataset_of.all():
            for x in dataset.sop.technology.all():
                if x.displayLabel not in technology:
                    technology.append(x.displayLabel)
        return technology
    
    def get_gender(self, study):
        genders = []
        for dataset in study.dataset_of.all():
            gender = dataset.bioMeta.sex
            if gender not in genders:
                genders.append(gender)
        return genders
    
    def get_biotype(self, study):
        biotypes = []
        for dataset in study.dataset_of.all():

            for x in dataset.bioMeta.biomaterialType.all():
                if x.displayLabel not in biotypes:
                    biotypes.append(x.displayLabel)
            #biotype = dataset.bioMeta.biomaterialType
            #if biotype not in biotypes:
                #biotypes.append(biotype)
        return biotypes

    def get_tissues(self, study):
        tissues = []
        for dataset in study.dataset_of.all():
            for x in dataset.bioMeta.tissue.all():
                if x.displayLabel not in tissues:
                    tissues.append(x.displayLabel)
        return tissues
    
    def get_pathology(self, study):
        pathologies = []
        for dataset in study.dataset_of.all():
            for x in dataset.bioMeta.pathology.all():
                if x.displayLabel not in pathologies:
                    pathologies.append(x.displayLabel)
        return pathologies
    
    def get_organs(self, study):
        organs = []
        for dataset in study.dataset_of.all():
            for x in dataset.bioMeta.organ.all():
                if x.displayLabel not in organs:
                    organs.append(x.displayLabel)
        return organs
    
    def get_species(self, study):
        species = []
        for dataset in study.dataset_of.all():
            for spe in dataset.bioMeta.species.all():
                if spe.displayLabel not in species:
                    species.append(spe.displayLabel)
        return species
    
    def get_dev_stage(self, study):
        devstage = []
        for dataset in study.dataset_of.all():
            for dev in dataset.bioMeta.developmentStage.all():
                if dev.displayLabel not in devstage:
                    devstage.append(dev.displayLabel)
        return devstage

    def get_authors(self, study):
        authors = []
        for article in study.article.all():
            for author in article.author.all() :
                if author.fullName not in authors:
                    authors.append(author.fullName)
        return authors
    
    def get_shorthand(self, study):
        shorthandList = []
        for article in study.article.all():
            shorthandList.append(article.shorthand)
        return shorthandList
    
    def get_pub_date(self, study):
        dates = [] 
        for article in study.article.all():
            date = article.releaseDate.year
            if date not in dates:
                dates.append(date)
        return dates
    
    def get_pub_pmids(self, study):
        pmids = [] 
        for article in study.article.all():
            pmid = article.pmid
            if pmid not in pmids:
                pmids.append(pmid)
        return pmids

    class Meta:
        model = Study
        read_only_fields = (
            "id",
            "studyId",
            "created_at",
            "created_by",
            "updated_at",
            "authors",
            "pub_date",
            "species",
            "shorthand",
            "gender",
            "dev_stage",
            "technology",
            "biomaterialType",
            "pathology",
            "experimentalDesign",
            "tissues",
            "organs",
            "pmids",
            'viewer'
        )
        fields = "__all__"
