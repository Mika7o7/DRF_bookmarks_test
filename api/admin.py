from django.contrib import admin
from .models import Bookmark, Collection

# Register your models here.

admin.site.register(Bookmark)
admin.site.register(Collection)