from django.conf import settings
from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from scilicium_django_react.users.api.views import UserViewSet, UserActivationView
from scilicium_django_react.studies.api.urls import *
from scilicium_django_react.datasets.api.views import *


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("v1/data", DatasetViewSet, basename="datasets")



app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    url(r'^v1/', include('djoser.urls')),
    url(r'^v1/', include('djoser.urls.authtoken')),
    url(r'^auth/users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', UserActivationView.as_view()),
    url(r'^v1/view_data', DataFormatPlotView.as_view(), name='view_data'),
]

# Route associated to data processing
urldata = [
    url(r'^v1/data/count', DataGetCellCount.as_view(), name='data_count'),
    url(r'^v1/data/sexrep', DataGetSexRepartition.as_view(), name='sex_rep'),
    url(r'^v1/data/cellcountbygroup', DataCellCountbyCluster.as_view(), name='cellcout_group'),
]

urlstudies = [
    url(r'^v1/projects/', projects_list, name='projects-list'),
    url(r'^v1/projects/<str:projectId>', projects_detail, name='projects-detail'),
    url(r'^v1/projects/public', projects_public, name='projects-public'),
    url(r'^v1/studies/', studies_list, name='projects-list'),
    url(r'^v1/studies/<str:studyId>', studies_detail, name='projects-detail'),
    url(r'^v1/studies/public', studies_public, name='projects-public'),
    
]

urlpatterns += urldata
urlpatterns += urlstudies