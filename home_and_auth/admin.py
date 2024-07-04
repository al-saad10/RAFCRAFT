from django.contrib import admin
from .models import *

class SliderItemImageInline(admin.TabularInline):
    model = SliderItemImage
    extra = 1

@admin.register(SliderItem)
class SliderItemAdmin(admin.ModelAdmin):
    inlines = [SliderItemImageInline]

admin.site.register(SliderItemImage)
