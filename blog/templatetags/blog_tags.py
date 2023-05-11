from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


# Для того чтобы быть допустимой библиотекой тегов, в каждом содержащем шаблонные теги модуле должна быть определена переменная с именем regis ter
# Эта переменная является экземпляром класса template.Library, и она используется для регистрации шаблонных тегов и фильтров приложения.
register = template.Library()


# В функцию был добавлен декоратор @register.simple_tag, чтобы зарегистрировать ее как простой тег.
@register.simple_tag
def total_posts():
    return Post.published.count()

# Inclusion tags включают другие шаблоны в текущий шаблон
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
# Теги включения должны возвращать словарь значений, который используется в качестве контекста для прорисовки заданного шаблона. 
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
# annotate() формируется набор запросов QuerySet, чтобы агрегировать общее число комментариев к каждому посту.
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))