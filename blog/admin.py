from django.contrib import admin
# Добавим модели на сайт одминистратора
from .models import Post, Comment

#В этот класс можно вставлять информацию о том, как показывать модель на сайте и как с ней взаимодействовать.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
#Атрибут list_display позволяет задавать поля модели, которые вы хотите показывать на странице списка объектов администрирования.
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title', )}
# Для поиска совпадений имен
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
