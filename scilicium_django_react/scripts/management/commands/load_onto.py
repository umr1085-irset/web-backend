from django.db import migrations
from django.apps import apps

from django.core.management.base import BaseCommand, CommandError

from scilicium_django_react.ontologies.models import *


def launch_import() :
    print('Start import ontologies')

class Command(BaseCommand):
    help = 'Load ontologies'

    def handle(self, *args, **options):
        launch_import()