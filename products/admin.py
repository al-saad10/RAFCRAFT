from django.contrib import admin
from .models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity_available')
    list_filter = ('quantity_available',)
    search_fields = ('product__name',)

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'product')
    list_filter = ('product',)
    search_fields = ('name', 'product__name')

admin.site.register(Category)
admin.site.register(SubCategory)
