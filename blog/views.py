from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib.postgres.search import SearchVector
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank



def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
# Поскольку здесь используется взаимосвязь многие-ко-многим, необходимо фильтровать записи по тегам, содержащимся в заданном списке, который в данном случае содержит только один элемент
# Операция __in используется для фильтрации объектов, которые содержат значение, указанное в списке
        post_list = post_list.filter(tags__in=[tag])
# Построничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
# добавили блок try и except, чтобы при извлечении страницы управлять
# исключением EmptyPage. Если запрошенная страница находится вне диапазона, то возвращаем последнюю страницу результатов
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
# Если page_number не целое число, то выдать пурвую страницу
        posts = paginator.page(1)
    except EmptyPage:
# Если page_number находится вне диапазона, то выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)

    return render(request,
                 'blog/post/list.html',
                 {'posts': posts,
                  'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True)
    # Форма для комментариев пользователями
    form = CommentForm()

    # Список схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})


class PostListView(ListView):
    """
    Альтернативное представление списка постов
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_share(request, post_id):
    # Извлекать пост по идентификатору id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    sent = False

# Когда пользователь заполняет форму и  передает ее методом POST на обработку, создается экземпляр формы с использованием переданных данных, 
# содержащихся в request.POST
    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
# После этого переданные данные валидируются методом is_valid() формы. Указанный метод проверяет допустимость введенных в форму данных и 
# возвращает значение True, если все поля содержат валидные данные. Если какое-либо поле содержит невалидные данные, то is_valid() возвращает значение False.
        if form.is_valid():
            # Поля формы успешно прошли валидацию. Отправить письмо
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
                      [cd['to']])
            sent = True
    else:
# Когда страница загружается в первый раз, представление получает запрос GET. В этом случае создается новый экземпляр класса EmailPostForm,
# который сохраняется в переменной form. 
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
# Конфигурация сервера электронной почты
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'vladis.alekandrov@gmail.com'
EMAIL_HOST_PASSWORD = 'khdomhjdvgzmqauv'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# @require_POST используется для проверки, был ли запрос выполнен с использованием метода HTTP-POST. 
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data = request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в бд
        comment = form.save(commit=False)
        # Назначить пост комменатрию
        comment.post = post
        # Сохранить комментарий в бд
        comment.save()
    return render(request, 'blog/post/comment.html',
                            {'post': post,
                             'form': form,
                             'comment': comment})


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query, config='spanish')
            results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank')
    return render(request,
                'blog/post/search.html',
                {'form': form,
                'query': query,
                'results': results})