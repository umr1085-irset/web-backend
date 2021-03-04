from rest_framework import viewsets 
from rest_framework.response import Response
from scilicium_django_react.studies.models import Project, Study
from scilicium_django_react.studies.api.serializers import *
from rest_framework import generics
from scilicium_django_react.users.models import User
from rest_framework import permissions
from rest_framework.decorators import action

class ProjectViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

        Additionally we also provide an extra `public` action to allow anyone to acces to public projects.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, permission_classes=[permissions.AllowAny],url_path='public', url_name='public')
    def public(self, request, *args, **kwargs):
        public = self.queryset.filter(status="PUBLIC")
        serializer = ProjectSerializer(public, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class StudyViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

        Additionally we also provide an extra `public` action to allow anyone to acces to public studies.
    """
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    lookup_field = 'studyId'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, permission_classes=[permissions.AllowAny],url_path='public', url_name='public')
    def public(self, request, *args, **kwargs):
        public = self.queryset.filter(status="PUBLIC")
        serializer = StudySerializer(public, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)