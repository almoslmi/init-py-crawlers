from django.conf.urls import patterns, include, url

from django.contrib import admin
from chat.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'watercooler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^chat/', chat_view),
    url(r'^login/', login_user),
)
