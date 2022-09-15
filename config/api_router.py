from django.conf import settings
from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from scilicium_django_react.users.api.views import UserViewSet, UserActivationView
from scilicium_django_react.studies.api.urls import *
from scilicium_django_react.datasets.api.views import *
from scilicium_django_react.studies.api.views import GetPublicStudies,StudyViewSet, ProjectViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("v1/datasets", DatasetViewSet, basename="datasets")
router.register("v1/studies", StudyViewSet, basename="studies")
router.register("v1/projects", ProjectViewSet, basename="studies")



app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    url(r'^v1/', include('djoser.urls')),
    url(r'^v1/', include('djoser.urls.authtoken')),
    url(r'^auth/users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', UserActivationView.as_view()),
    url(r'^v1/dataset/attributes/', GetLoomPlots.as_view(),name="dataset_attributes" ),
    url(r'^v1/dataset/statistics/', GetLoomStatistics.as_view(),name="dataset_statistics" ),
    url(r'^v1/dataset/genes/', GetLoomGenes.as_view(),name="dataset_genes" ),
    url(r'^v1/public/studies/', GetPublicStudies.as_view(),name="public_studies" ),
    url(r'^v1/public/datasets/', GetPublicDatasets.as_view(),name="public_datasets" ),
]
