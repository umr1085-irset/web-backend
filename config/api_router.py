from django.conf import settings
from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from scilicium_django_react.users.api.views import UserViewSet, UserActivationView
from scilicium_django_react.projects.api.views import ProjectViewSet
from scilicium_django_react.datasets.api.views import *


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("v1/projects", ProjectViewSet, basename="projects")
router.register("v1/datasets", DatasetViewSet, basename="datasets")
router.register("v1/data", DataViewSet, basename="datasets")



app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    url(r'^v1/', include('djoser.urls')),
    url(r'^v1/', include('djoser.urls.authtoken')),
    url(r'^auth/users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', UserActivationView.as_view()),
    url(r'^v1/view_data', DataFormatPlotView.as_view(), name='view_data'),
    url(r'^v1/datasets/public', DatasetAllViewSet.as_view(), name='public_datasets'),
]

# Route associated to data processing
urldata = [
    url(r'^v1/data/count', DataGetCellCount.as_view(), name='data_count'),
    url(r'^v1/data/sexrep', DataGetSexRepartition.as_view(), name='sex_rep'),
    url(r'^v1/data/cellcountbygroup', DataCellCountbyCluster.as_view(), name='cellcout_group'),
]


urlpatterns += urldata