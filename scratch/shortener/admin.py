from django.contrib import admin
from shortener.models import Url

class UrlAdmin(admin.ModelAdmin):
    list_display = ['httpurl', 'shorturl', 'is_vanity', 'click_count']
    list_filter = ['is_vanity', 'create_date', 'update_date']
    search_fields = ['httpurl']

admin.site.register(Url, UrlAdmin)