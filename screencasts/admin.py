from django.contrib import admin

# Register your models here.
from screencasts.models import ScreencastSection, Screencast

admin.site.register(ScreencastSection)
admin.site.register(Screencast)
