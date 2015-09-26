from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

from .models import Server

import main.kodi as KodiLookUp

# Create your views here.
def index(request):
  template = loader.get_template('main/index.html')
  return HttpResponse(template.render())

def kodi(request):
  serverList = Server.objects.all()

  serverStatusTable = []
  for server in serverList:
    serverStatusTable.append((server, KodiLookUp.Status(*server.conn())))

  context = {'kodi_server_list': serverStatusTable}
  return render(request, 'main/kodi.html', context)

def server(request, ident):
  server = Server.objects.get(pk=ident)
  recently_added_episodes = KodiLookUp.VideoLibrary_GetRecentlyAddedEpisodes(*server.conn())
  recently_added_movies = KodiLookUp.VideoLibrary_GetRecentlyAddedMovies(*server.conn())

  context = {'server':server, 'episodes':recently_added_episodes, 'movies':recently_added_movies}
  return render(request, 'main/kodi_server_index.html', context)

def tvindex(request, ident):
  server = Server.objects.get(pk=ident)
  tv_list = KodiLookUp.VideoLibrary_GetTVShows(*server.conn())
  context = {'server':server, 'tvshows':tv_list}
  return render(request, 'main/kodi_server_tv.html', context)

def tvshow(request, server_id, show_id):
  server = Server.objects.get(pk=server_id)
  season_list = KodiLookUp.VideoLibrary_GetSeasons(*server.conn(), show_id=show_id)
  context = {'server':server, 'seasons':season_list}
  return render(request, 'main/kodi_server_tv_show.html', context)

def tvseason(request, ident):
  raise NotImplementedError

def tvepisode(request, ident):
  raise NotImplementedError

def movies_index(request, ident):
  server = Server.objects.get(pk=ident)
  movie_list = KodiLookUp.VideoLibrary_GetMovies(*server.conn())
  context = {'server':server, 'movies':movie_list}
  return render(request, 'main/kodi_server_movies.html', context)

def movie(request, ident):
  raise NotImplementedError


# class KodiView(View):
    # def... VideoLibrary.GetRecentlyAddedEpisodes