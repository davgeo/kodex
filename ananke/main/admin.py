from django.contrib import admin

# Register your models here.
from .models import Server, Config

admin.site.register(Server)
admin.site.register(Config)