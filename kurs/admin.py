from multiprocessing.resource_tracker import register

from django.contrib import admin

from kurs import models

# Register your models here.
admin.site.register(models.Article)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Author)