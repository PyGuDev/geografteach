from django.conf import settings
from django.conf.urls import include
from django.urls import path
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls')),
    path('api/', include('blog.urls')),
    path('api/user/', include('user.urls')),
    path('api/lk/', include('task.urls')),
    path('api/lk/chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

