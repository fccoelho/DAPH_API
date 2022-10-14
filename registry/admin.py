from django.contrib import admin
from registry.models import Author, Manuscript, Article


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Author, AuthorAdmin)


class ManuscriptAdmin(admin.ModelAdmin):
    pass


admin.site.register(Manuscript, ManuscriptAdmin)


class ArticleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
