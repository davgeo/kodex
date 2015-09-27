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

def server(request, server_id):
  server = Server.objects.get(pk=server_id)
  recently_added_episodes = KodiLookUp.VideoLibrary_GetRecentlyAddedEpisodes(*server.conn())
  recently_added_movies = KodiLookUp.VideoLibrary_GetRecentlyAddedMovies(*server.conn())

  context = {'server':server, 'episodes':recently_added_episodes, 'movies':recently_added_movies}
  return render(request, 'main/kodi_server_index.html', context)

def tvindex(request, server_id):
  server = Server.objects.get(pk=server_id)
  tv_list = KodiLookUp.VideoLibrary_GetTVShows(*server.conn())
  context = {'server':server, 'tvshows':tv_list}
  return render(request, 'main/kodi_server_tv.html', context)

def tvshow(request, server_id, show_id):
  server = Server.objects.get(pk=server_id)
  season_list = KodiLookUp.VideoLibrary_GetSeasons(*server.conn(), show_id=show_id)
  context = {'server':server, 'seasons':season_list}
  return render(request, 'main/kodi_server_tv_show.html', context)

def tvseason(request, server_id, show_id, season_id):
  server = Server.objects.get(pk=server_id)
  episode_list = KodiLookUp.VideoLibrary_GetEpisodes(*server.conn(), show_id=show_id, season_id=season_id)
  context = {'server':server, 'episodes':episode_list}
  return render(request, 'main/kodi_server_tv_season.html', context)

def tvepisode(request, server_id, show_id, season_id, episode_id):
  server = Server.objects.get(pk=server_id)
  episode_list = KodiLookUp.VideoLibrary_GetEpisodes(*server.conn(), show_id=show_id, season_id=season_id)

  for episode in episode_list:
    if int(episode['episodeid']) == int(episode_id):
      name = episode['title']
      plot = episode['plot']

  context = {'server':server, 'episodes':episode_list, 'subheading': name, 'subtext': plot}
  return render(request, 'main/kodi_server_tv_season.html', context)

def movies_index(request, server_id):
  server = Server.objects.get(pk=server_id)
  movie_list = KodiLookUp.VideoLibrary_GetMovies(*server.conn())
  context = {'server':server, 'movies':movie_list}
  return render(request, 'main/kodi_server_movies.html', context)

def movie(request, server_id, movie_id):
  server = Server.objects.get(pk=server_id)
  movie_list = KodiLookUp.VideoLibrary_GetMovies(*server.conn())

  for movie in movie_list:
    if int(movie['movieid']) == int(movie_id):
      name = movie['title']
      plot = movie['plot']

  context = {'server':server, 'movies':movie_list, 'subheading': name, 'subtext': plot}
  return render(request, 'main/kodi_server_movies.html', context)

#def play(request, url):
  #print("PLAY")
  #server = Server.objects.get(pk=server_id)
  #KodiLookUp.Player_Play(*server.conn())
  #context = {'server':server}
  #return redirect(url)


# class KodiView(View):
    # def... VideoLibrary.GetRecentlyAddedEpisodes