from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^account/', include('userena.urls')),
    # (r'^messages/', include('userena.contrib.umessages.urls')),
    (r'^openmockup/', include('openmockup.urls')),
    url(r'^$',
        direct_to_template,
        {'template': 'static/promo.html'},
        name='promo'),
    (r'^i18n/', include('django.conf.urls.i18n')),
)

if settings.DEBUG:
    # ..
    urlpatterns += patterns(
            '',
            (
                r'^media/(?P<path>.*)$',
                'django.views.static.serve',
                {
                    'document_root': settings.MEDIA_ROOT,
                    'show_indexes': True,
                    }
                ),
            )
