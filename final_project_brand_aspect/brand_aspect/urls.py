from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls import url

urlpatterns = [
    path('', include('analytics.urls')),
    path('', include('reviews.urls')),
    path('', include('lexicons.urls')),
    path('', include('data_process.urls')),
    path('admin/', admin.site.urls),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

