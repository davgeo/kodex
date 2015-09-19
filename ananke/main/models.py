from django.db import models

# Create your models here.
class Server(models.Model):
  name = models.CharField(max_length=200)
  host = models.CharField(max_length=200)
  port = models.CharField(max_length=200)
  user = models.CharField(max_length=200)
  pwd = models.CharField(max_length=200)

  def __str__(self):
    return '{0} {1}:{2}'.format(self.name, self.host, self.port)

class Config(models.Model):
  activeServer = models.ForeignKey('Server')
  thumbnails = models.BooleanField()

  def __str__(self):
    return 'Active Server = {0}\n'.format(self.activeServer) \
         + 'Thumbnails = {0}'.format(self.thumbnails)
