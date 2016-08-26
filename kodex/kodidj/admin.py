from django.contrib import admin

# Register your models here.
from .models import Server, Config, StarredTV, StarredMovie

admin.site.register(Server)
admin.site.register(Config)
admin.site.register(StarredTV)
admin.site.register(StarredMovie)
