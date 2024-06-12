from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
)
