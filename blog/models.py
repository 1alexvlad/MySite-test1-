from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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
    slug = models.SlugField(max_length=250)
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

# По умолчанию посты отображаются в обратном порядке(от самых новых до самых старых). А мы это изменим, чтобы сортировал по 
# полю publish. Также предадим индекс этому полю, чтобы сократить время поиска запрошенных данных
    class Meta:
        ordering = ['-publish']
        indexes = [
        models.Index(fields=['-publish']),
    ]


    def __str__(self):
        return self.title