from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
  template = loader.get_template('main/index.html')
  return HttpResponse(template.render())

def kodi(request):
  template = loader.get_template('main/kodi.html')
  return HttpResponse(template.render())

# Class KodiView(View):
    # def... VideoLibrary.GetRecentlyAddedEpisodes