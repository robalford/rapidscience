"""rlp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from rlp.core import views
from rlp.sitemaps import sitemaps

handler500 = 'rlp.core.views.server_error'

urlpatterns = [
    url(r'^healthcheck/$', views.healthcheck),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('rlp.accounts.urls')),
    url(r'^bibliography/', include('rlp.bibliography.share_urls')),
    url(r'^bookmarks/', include('rlp.bookmarks.urls')),
    url(r'^comments/', include('rlp.discussions.urls')),
    url(r'^search/', include('rlp.search.urls')),
    url(r'^sitemap\.xml$',
        sitemap,
        {'sitemaps': sitemaps}),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^', include('cms.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns = [
        url(r'^500/$', views.server_error),
        url(r'^404/$', views.server_error, kwargs={'template': '404.html'})
    ] + urlpatterns
