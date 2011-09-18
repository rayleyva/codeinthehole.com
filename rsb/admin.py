from django.contrib import admin

from rsb.models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created', 'is_published')

admin.site.register(Article, ArticleAdmin)