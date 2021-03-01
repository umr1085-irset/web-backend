from .views import ProjectViewSet, StudyViewSet
from rest_framework import renderers

projects_list = ProjectViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
projects_detail = ProjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
projects_public = ProjectViewSet.as_view({
    'get': 'public'
})

studies_list = StudyViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
studies_detail = StudyViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
studies_public = StudyViewSet.as_view({
    'get': 'public'
})

