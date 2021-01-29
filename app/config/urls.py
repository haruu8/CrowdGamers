from django.contrib import admin
from django.urls import include, path
from . import settings
from django.conf.urls.static import static



admin.site.site_title = 'アプリ'
admin.site.site_header = 'アプリ管理画面'
admin.site.index_title = 'システム管理'



urlpatterns = [
    path('', include('clans.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
