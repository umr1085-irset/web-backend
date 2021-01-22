from rest_framework import viewsets 

from scilicium_django_react.projects.models import Project
from scilicium_django_react.projects.api.serializers import ProjectSerializer
from rest_framework import generics
from scilicium_django_react.users.models import User

class ProjectsList(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """

        queryset = Project.objects.filter(created_by=self.request.user.id)
        return queryset

class ProjectViewSet(viewsets.ModelViewSet):

    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)