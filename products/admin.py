from django.contrib import admin
from .models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category' , 'unitprice' , 'is_published')
    list_display_links = ('id', 'name')
    list_editable = ('is_published',)
    list_filter = ('category',)
    search_fields = ('name', 'category', 'unitprice')

admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'is_active' ,'date_added')
    list_display_links = ('id', 'category_name')
    list_editable = ('is_active',)
    list_filter = ('category_name',)
    search_fields = ('category_name',)


admin.site.register(Category, CategoryAdmin)
