from django.contrib import admin

# Register your models here.
from screencasts.models import ScreencastSection, Screencast


class ScreencastAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class ScreencastSectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(ScreencastSection, ScreencastSectionAdmin)
admin.site.register(Screencast, ScreencastAdmin)
