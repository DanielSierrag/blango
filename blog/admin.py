from django.contrib import admin
from . import models

# Register your models here.
class PostAdmin(admin.ModelAdmin):
  prepopulated_fields = {"slug": ("title",)}
  list_display = ('slug', 'published_at')

admin.site.register(models.Tag)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment)
admin.site.register(models.AuthorProfile)