from crypt import methods
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from scilicium_django_react.studies.models import Project, Study
from scilicium_django_react.studies.api.serializers import *
from rest_framework import generics
from scilicium_django_react.users.models import User
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


class ProjectViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

        Additionally we also provide an extra `public` action to allow anyone to acces to public projects.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'projectId'
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False,methods=['post'], permission_classes=[permissions.AllowAny],url_path='public', url_name='public')
    def post(self, request, *args, **kwargs):
        viewer = request.GET.get('viewer', None)
        print(viewer)
        public = self.queryset.filter(status="PUBLIC")
        serializer = ProjectSerializer(public, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    @action(detail=True, permission_classes=[permissions.AllowAny],url_path='view', url_name='view')
    def view(self, request, *args, **kwargs):
        project = self.get_object()
        if project.status == "PUBLIC" or project.created_by == self.request.user:
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        else :
            return Response('Your are not allowed to access this ressource', status=status.HTTP_403_FORBIDDEN)

class StudyViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

        Additionally we also provide an extra `public` action to allow anyone to acces to public studies.
    """
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    lookup_field = 'studyId'

    """ @action(detail=False, permission_classes=[permissions.AllowAny],url_path='public', url_name='public')
    def public(self, request, *args, **kwargs):
        public = self.queryset.filter(status="PUBLIC")
        serializer = StudyPublicSerializer(public, many=True)
        return Response(serializer.data) """

    """def perform_create(self, serializer):
        serializer.save(owner=self.request.user)"""
    
    @action(detail=True, permission_classes=[permissions.AllowAny],url_path='view', url_name='view')
    def view(self, request, *args, **kwargs):
        study = self.get_object()
        if study.status == "PUBLIC" or study.created_by == self.request.user:
            serializer = StudySerializer(study)
            return Response(serializer.data)
        else :
            return Response('Your are not allowed to access this ressource', status=status.HTTP_403_FORBIDDEN)

class GetPublicStudies(APIView):
    # Allow anyone to access
    # For test only
    queryset = Study.objects.all()
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        post_data = request.data
        viewerobj = get_object_or_404(Viewer,name=post_data['viewer'])
        public = self.queryset.filter(status="PUBLIC",viewer=viewerobj)
        serializer = StudyPublicSerializer(public, many=True)
        return Response(serializer.data) 