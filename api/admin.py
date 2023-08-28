from django.contrib import admin

from api.models import Article, Category, MainCategory, Query, PositivePoint, PenaltyPoint

admin.site.register(Category)
admin.site.register(MainCategory)
admin.site.register(PositivePoint)
admin.site.register(PenaltyPoint)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [ 'author', 'created']
    list_filter = ['created']


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = [ 'title', 'minimum', 'maximum']
    list_filter = ['title']
