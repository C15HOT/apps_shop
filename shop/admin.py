from django.contrib import admin
from django.contrib import admin
from .models import *


class AppAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']


admin.site.register(ScreenshotsApp)
admin.site.register(App, AppAdmin)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(News)
admin.site.register(Profile)