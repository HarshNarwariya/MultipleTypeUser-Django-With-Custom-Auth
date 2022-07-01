from django.contrib import admin
from writterPosts.models import Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner']
    search_fields = ['title',]

# admin.site.register(Post)