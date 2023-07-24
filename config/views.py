from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
import requests, json

def genome_browser(request):

    species = {
        'Homo sapiens': 'hg38',
        'Macaca mulatta': 'rheMac8',
        'Mus musculus':'mm10',
        'Rattus norvegicus':'rn6',
        'Canis lupus familiaris': 'canFam3',
        'Bos taurus': 'bosTau8',
        'Sus scrofa': 'susScr3',
        'Gallus gallus': 'galGal5',
        'Danio rerio': 'danRer10'
    }

    data = []
    base_rgv_url = "https://jbrowse-rgv.genouest.org/?data=data/sample_data/json/"
    base_ucsc_url = "https://genome.ucsc.edu/cgi-bin/hgTracks?db="


    for key, value in species.items():
        dict = {
            'name': key,
            'short': value,
            'image': 'images/species/genome_' + value + '.png',
            'rgv_url': base_rgv_url + value,
            'ucsc_url': base_ucsc_url + value,
        }

        #dict['studies'], dict['samples'] = _get_count(key)
        data.append(dict)

    return render(request, 'pages/genome_browser.html', {'species': data} )