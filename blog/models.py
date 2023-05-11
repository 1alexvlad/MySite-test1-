from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager



# создадим конкретно-прикладной менеджер, чтобы извлекать все посты, имеющие статус PUBLISHED.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                      .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

# Внутренний класс для черновиков (когда ты сохраняешь в черновиках без опубликования). draft - черновик  Доступными 
# вариантами статуса поста являются DRAFT и PUBLISHED. Их соответствующими значениями выступают DF и PB, 
# а их метками или читаемыми именами являются Draft и Published

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
# related_name позволяет обращаться к из связанных объектов к тем, от которых эта связь была создана
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    
    objects = models.Manager() # менеджер, применяется по умолчанию
    published = PublishedManager() # конкретно прикладной менеджер
    tags = TaggableManager()
    
# По умолчанию посты отображаются в обратном порядке(от самых новых до самых старых). А мы это изменим, чтобы сортировал по 
# полю publish. Также предадим индекс этому полю, чтобы сократить время поиска запрошенных данных
    class Meta:
        ordering = ['-publish']
        indexes = [
        models.Index(fields=['-publish']),
    ]


    def __str__(self):
        return self.title
# Функция reverse() будет формировать URL-адрес динамически, применяя имя URL-адреса, определенное в  шаблонах URL-адресов
# blog:post_detail, можно использовать глобально в  проекте, чтобы ссылаться на URL-адрес детальной информации о  посте
# Этот URL-адрес имеет обязательный параметр – id извлекаемого поста блога
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
    

# разработки модели для хранения комментариев пользователей к постам
class Comment(models.Model):
    post = models.ForeignKey(Post, 
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'