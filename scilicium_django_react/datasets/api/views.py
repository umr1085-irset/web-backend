import os

from rest_framework import viewsets 
from rest_framework import status, permissions
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django.core.files import File
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import permissions
from django.db.models import Q
from django.conf import settings

from matplotlib import pyplot as plt
from scilicium_django_react.datasets.models import Dataset, Loom
from scilicium_django_react.studies.models import Study, Viewer
from scilicium_django_react.datasets.api.serializers import DatasetSerializer, LoomSerializer, PublicDatasetSerializer, BasicDatasetSerializer
from scilicium_django_react.users.models import User
from scilicium_django_react.utils.loom_reader import *
from scilicium_django_react.utils.chartjsCreator import *
from scilicium_django_react.utils.plotlyCreator import *

class GetGenomeBrowser(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kw):
        print('test')
        species = {
            'Homo sapiens': 'hg38',
            'Macaca mulatta': 'rheMac8',
            'Mus musculus':'mm10',
            'Rattus norvegicus':'rn6',
            'Canis lupus familiaris': 'canFam3',
            'Bos taurus': 'bosTau8',
            'Sus scrofa': 'susScr3',
            'Gallus gallus': 'galGal5',
            'Danio rerio': 'danRer10'
        }

        data = []
        base_rgv_url = "https://jbrowse-rgv.genouest.org/?data=data/sample_data/json/"
        base_ucsc_url = "https://genome.ucsc.edu/cgi-bin/hgTracks?db="

        for key, value in species.items():
            d = {
                'name': key,
                'short': value,
                #'image': 'images/species/genome_' + value + '.png',
                'rgv_url': base_rgv_url + value,
                #'ucsc_url': base_ucsc_url + value,
            }

            #d['studies'], d['samples'] = _get_count(key)
            data.append(d)
        print(data)
        return Response(data, status=status.HTTP_200_OK)


class GetPublicDatasets(APIView):
    # Allow anyone to access
    # For test only
    queryset = Dataset.objects.all()
    #querysetStudy = Study.objects.all()
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        post_data = request.data
        #viewerobj = get_object_or_404(Viewer,name=post_data['viewer'])
        #filter on viewer for the STUDY
        viewerobj = get_object_or_404(Viewer,name=post_data['viewer']) 
        #publicStudies = self.querysetStudy.filter(status="PUBLIC",viewer=viewerobj)
        publicDatasets= self.queryset.filter(status="PUBLIC", study__viewer=viewerobj)
        serializer = PublicDatasetSerializer(publicDatasets,many=True)
        return Response(serializer.data) 

class DatasetViewSet(viewsets.ModelViewSet):

    serializer_class = DatasetSerializer
    queryset = Dataset.objects.all()
    lookup_field = 'datasetId'
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, permission_classes=[permissions.AllowAny],url_path='filters', url_name='filters')
    def filters(self, request, *args, **kwargs):
        dataset = self.get_object()
        if dataset.status == "PUBLIC" or dataset.created_by == self.request.user:
            key = request.GET.get('key', None)
            value = request.GET.get('value', None)

            data = get_object_or_404(Loom,id=dataset.loom.id)
            if key == "row":
                values = get_ra(data.file.path,key=value,unique=True)
                return  Response({"values":values}, status=status.HTTP_200_OK)
            if key == "col":
                values = get_ca(data.file.path,key=value,unique=True)
                return  Response({"values":values}, status=status.HTTP_200_OK)
            else :
                return Response('Key value not recognize', status=status.HTTP_403_FORBIDDEN)
        else :
            return Response('Your are not allowed to access this ressource', status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, permission_classes=[permissions.AllowAny],url_path='view', url_name='view')
    def view(self, request, *args, **kwargs):
        dataset = self.get_object()
        if dataset.status == "PUBLIC" or dataset.created_by == self.request.user:
            serializer = DatasetSerializer(dataset)
            return Response(serializer.data)
        else :
            return Response('Your are not allowed to access this ressource', status=status.HTTP_403_FORBIDDEN)
    

    @action(detail=True, permission_classes=[permissions.AllowAny],url_path='overview', url_name='overview')
    def overview(self, request, *args, **kwargs):
        dataset = self.get_object()
        if dataset.status == "PUBLIC" or dataset.created_by == self.request.user:
            serializer = BasicDatasetSerializer(dataset)
            return Response(serializer.data)
        else :
            return Response('Your are not allowed to access this ressource', status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, permission_classes=[permissions.AllowAny],url_path='download', url_name='download')
    def download(self, request, *args, **kwargs):
        dataset = self.get_object()
        if dataset.status == "PUBLIC" or dataset.created_by == self.request.user:
            #print(dataset.loom.name)
            from scilicium_django_react.utils.utils import zip_results
            user_type = "user"
            if dataset.created_by and dataset.created_by.is_superuser:
                user_type = "admin"

            tmp_folder =  "{}/datasets/loom/{}/{}/".format(settings.MEDIA_ROOT,user_type, dataset.loom.id)
            if not os.path.exists(tmp_folder + 'archive.zip'):
                zip_results(tmp_folder)

            response = FileResponse(open(tmp_folder +'archive.zip', 'rb'))
            response['Content-Type'] = "application/zip"
            response['Content-Disposition'] = 'attachment; filename={}_archive.zip'.format(dataset.datasetId)
            response['Content-Transfer-Encoding'] = "binary"
            response['Content-Length'] = os.path.getsize(tmp_folder +'archive.zip')

            return response

        else :
            return Response('Your are not allowed to download this ressource', status=status.HTTP_403_FORBIDDEN)
    
    @action(detail=False, permission_classes=[permissions.AllowAny],url_path='public', url_name='public')
    def public(self, request, *args, **kwargs):
        public = self.queryset.filter(status="PUBLIC")
        serializer = PublicDatasetSerializer(public, many=True)
        return Response(serializer.data)
        
    
    

class LoomViewSet(viewsets.ModelViewSet):
    serializer_class = LoomSerializer
    queryset = Loom.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class GetLoomStatistics(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kw):
        post_data = request.data
        data_id = post_data['id']
        filters = post_data['filters']

        # Get data
        data = get_object_or_404(Loom,id=data_id)
        response_data = dict()
        reduced = False
        if data.light_file:
            loomfile = data.light_file.path
            reduced = True
        else:
            loomfile = data.file.path


        if (filters['ca']!={}) or (filters['ra']!={}):
            cidx_filter, ridx_filter = get_filter_indices(loomfile,filters)
        else:
            cidx_filter, ridx_filter = (None,None)
        
        ngenes, ncells = get_shape(loomfile)
        try:
            response_data['col_val'] = len(cidx_filter)
        except:
            response_data['col_val'] = ncells
        try:
            response_data['row_val'] = len(ridx_filter)
        except:
            response_data['row_val'] = ngenes

        response_data['reduced'] = reduced
        response = Response(response_data, status=status.HTTP_200_OK)
        return response

class GetLoomGenes(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kw):
        post_data = request.data
        data_id = post_data['id']
        filters = post_data['filters']

        #Remove potential Symbol in filter
        filters['ra'] = filters['ra'].pop('Symbol', None)

        data = get_object_or_404(Loom,id=data_id)
        response_data = dict()

        reduced = False
        if data.light_file:
            loomfile = data.light_file.path
            reduced = True
        else:
            loomfile = data.file.path

        response_data['reduced'] = reduced
        if (filters['ca']!={}) or (filters['ra']=={}):
            cidx_filter, ridx_filter = get_filter_indices(loomfile,filters)
        else:
            cidx_filter, ridx_filter = (None,None)

        if 'method' in post_data and post_data['method'] !='custom':
            gene_selection = post_data['method']
            response_data["genes"] = auto_get_symbols(loomfile,n=6,ridx_filter=ridx_filter,cidx_filter=cidx_filter,method=gene_selection)
            response = Response(response_data, status=status.HTTP_200_OK)
            return response
        else:
            response_data["genes"] = get_ra(loomfile,unique=True,ridx_filter=ridx_filter)
            response = Response(response_data, status=status.HTTP_200_OK)
            return response
        

        
        

class GetLoomPlots(APIView):
    """
        Associated view for the REACT CellCountComponent component
        User request validation (data public or user == data owner)
        [GET] --> data id
        [RESPONSE] --> HTTP_403_Forbidden (data private && user not owner)
        [RESPONSE] --> HTTP_200_OK  (data public | user owner)
        [RSPONSE][data] : {
            count : int(numberOfcells) or int(numberOfSamples),
            name : str(data.name)
        }

    """
    # Allow anyone to access
    # For test only
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kw):

        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        #print(request.data)
        post_data = request.data
        data_id = post_data['id']
        attrs = post_data['attrs']
        style = post_data['style']
        genes_menu = 'undefined'
        log = False # rajouter dans le post
        scale = False # rajouter dans le post
        if 'menu' in post_data:
            genes_menu = post_data['menu']
        filters = post_data['filters']
        symbols = []
        if 'symbols' in post_data :
            symbols=post_data['symbols']
        reduction = None
        if 'reduction' in filters :
            if filters["reduction"] != '':
                reduction = filters["reduction"]
        
        # Get data
        data = get_object_or_404(Loom,id=data_id)
        reduced = False
        if data.light_file:
            loomfile = data.light_file.path
            reduced = True
        else:
            loomfile = data.file.path

        if (filters['ca']!={}) or (filters['ra']!={}):
            cidx_filter, ridx_filter = get_filter_indices(loomfile,filters)
        else:
            cidx_filter, ridx_filter = (None,None)
        
        if 'ra' in filters :
            if 'Symbol' in filters['ra'] and len(filters['ra']['Symbol'])> 0 and len(symbols)==0:
                symbols = filters['ra']['Symbol']


        # Data status check + user ownership == TO DO check status from dataset
        #if data.status == "PRIVATE" and data.created_by != self.request.user :
        #    response = Response({"msg":"You are not allowed to access this ressource"}, status=status.HTTP_403_FORBIDDEN)
        #    return response
        # Bonjour PAul C'est Thomas qui te parle ;)
        
        response_data = dict()
        response_data["name"] = data.name
        response_data["classes"] = data.classes
        response_data['reduced'] = reduced
        #print(ridx_filter)
        #print(filters['ra'])
        if genes_menu != 'undefined':
            response_data["genes_menu"] = get_ra(loomfile,unique=True,ridx_filter=ridx_filter)
        if style =="scatter":
            response_data['chart'] = json_scatOrSpat(style,loomfile,color=attrs,reduction=reduction,cidx_filter=cidx_filter)
            response_data['style'] = "scatter"
            response = Response(response_data, status=status.HTTP_200_OK)
            return response

        elif style=='hexbin':
            response_data['chart'] = json_scatOrSpat(style,loomfile, reduction=reduction, color=attrs, returnjson=True, cidx_filter=cidx_filter)
            response_data['style'] = 'hexbin'
            response = Response(response_data, status=status.HTTP_200_OK)
            return response

        elif style=='dot':
            response_data['chart'] = dotplot_json(loomfile,attribute=attrs,symbols=symbols,cidx_filter=cidx_filter,ridx_filter=ridx_filter,log=log,scale=scale)
            response_data['style'] = 'dot'
            response = Response(response_data, status=status.HTTP_200_OK)
            return response

        elif style=='violin':
            response_data['chart'] = violin_json(loomfile,attribute=attrs,symbols=symbols,cidx_filter=cidx_filter,log=log)
            response_data['style'] = 'violin'
            response = Response(response_data, status=status.HTTP_200_OK)
            return response
        
        elif style=='density':
            #response_data['chart'],response_data['legend'] = json_density(loomfile,reduction=reduction,ca=attrs,symbols=symbols,cidx_filter=cidx_filter)
            response_data['chart'] = json_scatOrSpat(style,loomfile,color=attrs,reduction=reduction,cidx_filter=cidx_filter)
            response_data['style'] = 'density'
            response = Response(response_data, status=status.HTTP_200_OK)
            return response

        else :
            if attrs == 'undefined' :
                attrs = [response_data["classes"][0]]
            else:
                attrs = [attrs]
            data = json.loads(json_component_chartjs(loomfile,style=style,attrs=attrs,cidx_filter=cidx_filter))
            response_data['chart'] = data["chart"]
            response_data['style'] = data["style"]
            response_data['options'] = data["options"]

            response = Response(response_data, status=status.HTTP_200_OK)
            return response
