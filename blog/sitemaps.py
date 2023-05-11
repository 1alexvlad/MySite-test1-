from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()
    
# Метод lastmod получает каждый возвращаемый методом items() объект и возвращает время последнего изменения объекта
    def lastmod(self, obj):
        return obj.updated