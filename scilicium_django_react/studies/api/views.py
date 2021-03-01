from rest_framework import viewsets 

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

    @action(detail=True, methods=['get'],permission_classes=[permissions.AllowAny])
    def public(self, request, *args, **kwargs):
        return self.queryset.filter(status="PUBLIC")

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'],permission_classes=[permissions.AllowAny])
    def public(self, request, *args, **kwargs):
        return self.queryset.filter(status="PUBLIC")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)