from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    fields = ['author', 'date_posted', 'title', 'content']
    list_display = ['title', 'author', 'date_posted']
    list_filter = ['author', 'date_posted']
    search_fields = ['content', 'title']


admin.site.register(Post, PostAdmin)
