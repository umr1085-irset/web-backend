from rest_framework import viewsets 
from rest_framework import status, permissions
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from django.db.models import Q

from scilicium_django_react.datasets.models import Dataset, Study
from scilicium_django_react.datasets.api.serializers import DatasetSerializer, StudyHudeCaSerializer
from scilicium_django_react.users.models import User
from scilicium_django_react.utils.loom_reader import *
from scilicium_django_react.utils.chartjsCreator import *
from scilicium_django_react.utils.plotlyCreator import *



class StudyViewSet(viewsets.ModelViewSet):

    serializer_class = StudyHudeCaSerializer
    queryset = Study.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

class DatasetViewSet(viewsets.ModelViewSet):

    serializer_class = DatasetSerializer
    queryset = Dataset.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(Q(created_by=self.request.user) |Q( status="PUBLIC" ) )


class StudyAllViewSet(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    queryset = Study.objects.all()
    serializer_class = StudyHudeCaSerializer

    def get(self,request):
        serializer = StudyHudeCaSerializer(self.queryset.filter(status="PUBLIC"), many=True)
        return JsonResponse(serializer.data, safe=False)

class DataFormatPlotView(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        data_id = request.GET.get('id', None)
        selected_class = request.GET.get('cluster', None)
        plot_type= request.GET.get('plot', None)
        reader_type = request.GET.get('reader', None)

        # Any URL parameters get passed in **kw
        data = Dataset.objects.get(id=data_id)
        
        # TO DO
        # Check if data type is compatible with the plot_type
        # Add new model --> Display.plot_type

        # TO DO
        # Select utils reader according data_type
        # Add new model --> Display.reader

        loom_file = data.upload.path 
        response_data = dict()
        response_data["name"] = data.name

         # Fonction according data type
        if data.data_type.name == "Loom" :
            loom_file = data.upload.path
        # Get display type
        
        if plot_type == "scattergl" :
            if reader_type =="plotly":
                 plot = scatterFromLoom(loom_file,selected_class)
            else :
                response = Response({"msg":"Display not allowed"}, status=status.HTTP_403_FORBIDDEN)
                return response
        else :
            response = Response({"msg":"Display not allowed"}, status=status.HTTP_403_FORBIDDEN)
            return response

        response_data["chart"] = plot["chart"]
        response_data["title"] = plot["title"]
        response_data["layout"] = plot["layout"]
        response = Response(response_data, status=status.HTTP_200_OK)
        return response
    
class DataGetCellCount(APIView):
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

    def get(self, request, *args, **kw):

        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part

        data_id = request.GET.get('id', None)
        #data_id=1
        # Get data
        print("DATA ID     " + str(data_id))
        data = get_object_or_404(Dataset,id=data_id)

        # Data status check + user ownership
        #if data.status == "PRIVATE" and data.created_by != self.request.user :
        #    response = Response({"msg":"You are not allowed to access this ressource"}, status=status.HTTP_403_FORBIDDEN)
        #    return response
        
        
        response_data = dict()
        response_data["name"] = data.name

        # Fonction according data type
        #if data.data_type.name == "Loom" :
        #    loom_file = data.upload.path
        #    response_data["count"] = getCellCount(loom_file)

        response = Response(response_data, status=status.HTTP_200_OK)
        return response

class DataGetSexRepartition(APIView):
    """
        Associated view for the REACT SexRepartitionComponent component
        User request validation (data public or user == data owner)
        [GET] --> data id
        [GET] --> type of graph
        [GET] --> graph reader
        [RESPONSE] --> HTTP_403_Forbidden (data private && user not owner)
        [RESPONSE] --> HTTP_200_OK  (data public | user owner)
        [RSPONSE][data] : {
            graph : obj(graph),
        }

    """
    # Allow anyone to access
    permission_classes = (permissions.AllowAny,)
    #authentication_classes = ()

    def get(self, request, *args, **kw):

        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part

        data_id = request.GET.get('id', None)
        plot_type = request.GET.get('plot', None)
        reader_type = request.GET.get('reader', None)

        # Get data
        data = get_object_or_404(Dataset,id=data_id)

        # Data status check + user ownership
        if data.status == "PRIVATE" and data.created_by != self.request.user :
            response = Response({"msg":"You are not allowed to access this ressource"}, status=status.HTTP_403_FORBIDDEN)
            return response
        
        
        response_data = dict()
        response_data["name"] = data.name
        response_data["plot_type"] = plot_type
        response_data["reader"] = reader_type

        # Fonction according data type
        if data.data_type.name == "Loom" :
            loom_file = data.upload.path
            repartition_cluster = getRepartitionCluster(loom_file,',') # For test Need to chage in getSexRepartition
        # Get display type
        if plot_type == "pie" :
            if reader_type =="plotly":
                response_data["chart"] = createPiePlotly(repartition_cluster)
            if reader_type =="chartjs":
                response_data["chart"] = createPieChart(repartition_cluster)
        
        if plot_type == "doughnut" :
            if reader_type =="plotly":
                response_data["chart"] = createPiePlotly(repartition_cluster)
            if reader_type =="chartjs":
                response_data["chart"] = createDoughnutChart(repartition_cluster)
        
        if plot_type == "scattergl" :
            if reader_type =="plotly":
                print("scattergl plotly")
            if reader_type =="chartjs":
                print("scattergl chartjs")
        
        if plot_type == "bar" :
            if reader_type =="plotly":
                print("bar plotly")
            if reader_type =="chartjs":
                print("bar chartjs")


        response = Response(response_data, status=status.HTTP_200_OK)
        return response

class DataCellCountbyCluster(APIView):
    """
        Associated view for the REACT DevStageComponent component
        User request validation (data public or user == data owner)
        [GET] --> data id
        [GET] --> type of graph
        [GET] --> graph reader
        [GET] --> cluster name
        [RESPONSE] --> HTTP_403_Forbidden (data private && user not owner)
        [RESPONSE] --> HTTP_200_OK  (data public | user owner)
        [RSPONSE][data] : {
            graph : obj(graph),
        }

    """
    # Allow anyone to access
    permission_classes = (permissions.AllowAny,)
    #authentication_classes = ()

    def get(self, request, *args, **kw):

        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part

        data_id = request.GET.get('id', None)
        plot_type = request.GET.get('plot', None)
        reader_type = request.GET.get('reader', None)
        cluster = request.GET.get('cluster', None)


        # Get data
        data = get_object_or_404(Dataset,id=data_id)

        # Data status check + user ownership
        if data.status == "PRIVATE" and data.created_by != self.request.user :
            response = Response({"msg":"You are not allowed to access this ressource"}, status=status.HTTP_403_FORBIDDEN)
            return response
        
        
        response_data = dict()
        response_data["name"] = data.name
        response_data["plot_type"] = plot_type
        response_data["reader"] = reader_type

        # Fonction according data type
        if data.data_type.name == "Loom" :
            loom_file = data.upload.path
            repartition_cluster = getCellCountByCluster(loom_file,cluster) # For test Need to chage in getSexRepartition
        # Get display type
        if plot_type == "pie" :
            if reader_type =="plotly":
                response_data["chart"] = createPiePlotly(repartition_cluster)
            if reader_type =="chartjs":
                response_data["chart"] = createPieChart(repartition_cluster)
        
        if plot_type == "scattergl" :
            if reader_type =="plotly":
                print("scattergl plotly")
            if reader_type =="chartjs":
                print("scattergl chartjs")
        
        if plot_type == "bar" :
            if reader_type =="plotly":
                print("bar plotly")
            if reader_type =="chartjs":
               response_data["chart"] = createBarChart(repartition_cluster)


        response = Response(response_data, status=status.HTTP_200_OK)
        return response