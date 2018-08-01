from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from genus.urls import urlpatterns as genus_urls
from mainpage.urls import urlpatterns as mainpage_urls
from species.urls import urlpatterns as species_urls

urlpatterns = [
    url(r'^',
        include(genus_urls, namespace='genus_app', app_name='genus')),
    url(r'^mainpage/',
        include(mainpage_urls, namespace='mainpage_app', app_name='mainpage')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^species/',
        include(species_urls, namespace='species_app', app_name='species')),
    url(r'^tinymce/', include('tinymce.urls')),
]\
              + static(settings.STATIC_URL,
                       document_root=settings.STATIC_ROOT)\
              + static(settings.MEDIA_URL,
                       document_root=settings.MEDIA_ROOT)
