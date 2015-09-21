from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

from .models import Server

# Create your views here.
def index(request):
  template = loader.get_template('main/index.html')
  return HttpResponse(template.render())

def kodi(request):
  serverList = Server.objects.all()

  serverStatusTable = []
  for server in serverList:
    serverStatusTable.append((server, server.CheckStatus()))

  context = {'kodi_server_list': serverStatusTable}
  return render(request, 'main/kodi.html', context)

def server(request, ident):
  server = Server.objects.get(pk=ident)
  recently_added_episodes = server.GetRecentlyAddedEpisodes()

  context = {'server':server, 'episodes':recently_added_episodes}
  return render(request, 'main/kodi_server_index.html', context)

def tv(request, ident):
  server = Server.objects.get(pk=ident)
  context = {'server':server}
  return render(request, 'main/kodi_server_index.html', context)

def movies(request, ident):
  server = Server.objects.get(pk=ident)
  context = {'server':server}
  return render(request, 'main/kodi_server_index.html', context)

# class KodiView(View):
    # def... VideoLibrary.GetRecentlyAddedEpisodes