from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    (r'^elections/2016/admin/', include(admin.site.urls)),
)