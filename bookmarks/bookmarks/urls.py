from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('images/', include('images.urls', namespace='images')),

]

# Эти строки добавляют обработку запросов к медиа-файлам (изображениям, видео и т.д.), если проект находится в режиме отладки (DEBUG=True). 
# Функция static() из модуля создает URL-шаблон для обработки запросов к медиа-файлам, указанным в настройках проекта (MEDIA_URL и MEDIA_ROOT). 
# document_root=settings.MEDIA_ROOT указывает путь к корневой директории, где хранятся медиа-файлы. 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)