from django.contrib import admin
from .models import Post
from django.db import models


class AdminModel(admin.ModelAdmin):
    list_display = ['title', 'content', 'date_posted', 'author']


admin.site.register(Post, AdminModel)
