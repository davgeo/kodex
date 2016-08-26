from django.db import models

# Create your models here.

# Server settings
class Server(models.Model):
  name = models.CharField(max_length=200)
  host = models.CharField(max_length=200)
  port = models.CharField(max_length=200)
  user = models.CharField(max_length=200)
  pwd = models.CharField(max_length=200)

  def __str__(self):
    return '{0} {1}:{2}'.format(self.name, self.host, self.port)

  def conn(self):
    return (self.host, self.port, self.user, self.pwd)

# Starred items
class StarredBase(models.Model):
  starred_id = models.IntegerField(primary_key=True)

  class Meta:
    abstract = True

  def __str__(self):
    return 'ID: {}'.format(self.starred_id)

  def get_id(self):
    return self.starred_id

class StarredTV(StarredBase):
  pass

class StarredMovie(StarredBase):
  pass

# Configuration
class Config(models.Model):
  activeServer = models.ForeignKey('Server')
  thumbnails = models.BooleanField()

  def __str__(self):
    return 'Active Server = {0}\n'.format(self.activeServer) \
         + 'Thumbnails = {0}'.format(self.thumbnails)
