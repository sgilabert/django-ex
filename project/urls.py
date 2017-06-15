from django.conf.urls import include, url
from django.contrib import admin
from imapclient.views import index

from welcome.views import health

urlpatterns = [
    url(r'^$', index),
    url(r'^health$', health),
    url(r'^admin/', include(admin.site.urls)),
]
