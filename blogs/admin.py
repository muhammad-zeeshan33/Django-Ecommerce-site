from django.contrib import admin
from .models import Blog
from .models import Comment
class blogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author','published', 'created')
    list_display_links = ('id', 'title')
    list_filter = ('author',)
    list_editable = ('published',)
    search_fields = ('title', 'author')

admin.site.register(Blog, blogAdmin)
admin.site.register(Comment)
