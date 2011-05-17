
# django import
from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

# openmockup import
from openmockup import views

urlpatterns = patterns('',

    url(r'^list/$',
        views.mockup_list,
        name='openmockup_list'),

    url(r'^trash/$',
        views.mockup_list,
        {'trash': True},
        name='openmockup_trash'),

    url(r'^new/$',
        views.mockup_compose,
        name='openmockup_new'),

    url(r'^edit/(?P<mockup_id>[\d]+)/$',
        views.mockup_compose,
        name='openmockup_edit'),

    url(r'^view/(?P<mockup_id>[\d]+)/$',
        views.mockup_detail,
        name='openmockup_detail'),

    url(r'^remove/$',
        views.mockup_remove,
        name='openmockup_remove'),

    url(r'^unremove/$',
        views.mockup_remove,
        {'undo': True},
        name='openmockup_unremove'),

    url(r'^$',
        redirect_to,
        {'url': 'list/'},
        name='openmockups'),
)
