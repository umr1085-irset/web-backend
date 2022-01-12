from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from scilicium_django_react.studies.models import *
from scilicium_django_react.datasets.api.serializers import DatasetSerializer
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
    dataset_of = DatasetSerializer(many=True, read_only=True)
    created_by = GetFullUserSerializer(many=False, read_only=True)
    contributor = ContributorSerializer(many=False, read_only=True)

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
    gender = serializers.SerializerMethodField('get_gender')
    pmids = serializers.SerializerMethodField('get_pub_pmids')
    created_by = GetFullUserSerializer(many=False, read_only=True)

    def get_technology(self, study):
        technology = []
        for dataset in study.dataset_of.all():
            for x in dataset.sop.technology.all():
                if x.ontologyLabel not in technology:
                    technology.append(x.ontologyLabel)
        return technology
    
    def get_gender(self, study):
        genders = []
        for dataset in study.dataset_of.all():
            gender = dataset.bioMeta.sex
            if gender not in genders:
                genders.append(gender)
        return genders
    
    def get_tissues(self, study):
        tissues = []
        for dataset in study.dataset_of.all():
            for x in dataset.bioMeta.tissue.all():
                if x.ontologyLabel not in tissues:
                    tissues.append(x.ontologyLabel)
            for x in dataset.bioMeta.organ.all():
                if x.ontologyLabel not in tissues:
                    tissues.append(x.ontologyLabel)
        return tissues
    
    def get_species(self, study):
        species = []
        for dataset in study.dataset_of.all():
            for spe in dataset.bioMeta.species.all():
                if spe.ontologyLabel not in species:
                    species.append(spe.ontologyLabel)
        return species
    
    def get_dev_stage(self, study):
        devstage = []
        for dataset in study.dataset_of.all():
            for dev in dataset.bioMeta.developmentStage.all():
                if dev.ontologyLabel not in devstage:
                    devstage.append(dev.ontologyLabel)
        return devstage

    def get_authors(self, study):
        authors = []
        for article in study.article.all():
            for author in article.author.all() :
                if author.fullName not in authors:
                    authors.append(author.fullName)
        return authors
    
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
            "technology",
            "species",
            "dev_stage",
            "gender",
            "tissues",
            "pmids",
        )
        fields = "__all__"