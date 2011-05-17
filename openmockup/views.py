
# python import
from datetime import datetime

# django import
from django.core.urlresolvers import reverse
# ..
from django.contrib.auth import decorators, models
from django.contrib import messages
# ..
from django.http import Http404
# ..
from django.shortcuts import get_object_or_404, redirect
# ..
from django.template import loader
# ..
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
# ..
from django.views.decorators import http
from django.views.generic import list_detail, simple

# openmockup import
from openmockup.models import Mockup
from openmockup.forms import ComposeForm

# TODO manage settings
# from openmockup import settings as openmockup_settings


@decorators.login_required
def mockup_list(request, page=1, paginate_by=50, trash=False,
                 fallback_template_name='openmockup/mockup_list.html',
                 extra_context=None, **kwargs):

    # get asked or current page
    try:
        page = int(request.GET.get('page', None))
    except TypeError, ValueError:
        page = page

    # prepare query
    _queryset = Mockup.objects.filter(owner=request.user,
                                            deleted_at__isnull=not trash)

    # ensure dict
    if extra_context is None:
        extra_context = dict()
    extra_context['trash'] = trash

    # Get the right template
    _tmp_ext = '_trash' if trash is True else ''
    template_loader = loader.select_template(["openmockup/mockup_list%s.html"\
                                              % _tmp_ext, fallback_template_name])

    # list in template
    return list_detail.object_list(request,
                                   queryset=_queryset,
                                   paginate_by=paginate_by,
                                   page=page,
                                   template_name=template_loader.name,
                                   extra_context=extra_context,
                                   template_object_name='mockup',
                                   **kwargs)


@decorators.login_required
def mockup_detail(request, mockup_id,
                        template_name='openmockup/mockup_detail.html',
                        threaded=False, extra_context=None):

    # get asked mockup
    _mockup = get_object_or_404(Mockup, pk=mockup_id)

    # TODO - manage view rule here

    # ensure extra dict
    if extra_context is None:
        extra_context = dict()

    # update extra dict
    extra_context['mockup'] = _mockup

    # render
    return simple.direct_to_template(request, template_name,
                                     extra_context=extra_context)


@decorators.login_required
def mockup_compose(request, mockup_id=None, mockup_form=None,
                         success_url='openmockup_list',
                         template_name='openmockup/mockup_form.html',
                         extra_context=None):
    # ensure compose form
    mockup_form = ComposeForm if mockup_form is None else mockup_form

    # do save
    _mockup = None if mockup_id is None\
            else get_object_or_404(Mockup, pk=mockup_id)

    # request facotry
    if request.method == 'POST':
        # init form with values
        _form = mockup_form(request.POST)

        # validaity check
        if _form.is_valid():
            # do save
            _form.save(request.user, mockup=_mockup)
            # if userena_settings.USERENA_USE_MESSAGES:
            messages.success(request, _('Mockup saved.'),
                             fail_silently=True)
            # prepare redirect
            _next_redirect = request.REQUEST.get('next', False)
            # do redirect
            if _next_redirect:
                return redirect(_next_redirect)
            else:
                return redirect(reverse(success_url))
        else:
            pass
    else:
        # get asked mockup
        _mockup = get_object_or_404(Mockup, pk=mockup_id)
        # ..
        _initial = {'content': _mockup.content}
        # ..
        _form = mockup_form(initial=_initial)

    # ensure extra
    if extra_context is None:
        extra_context = dict()
    # extra update
    extra_context['new'] = mockup_id is None
    extra_context['form'] = _form

    # render
    return simple.direct_to_template(request, template_name,
                                     extra_context=extra_context)


@decorators.login_required
@http.require_http_methods(['POST'])
def mockup_remove(request, undo=False):

    # get keys to remove
    _mockup_pks = request.POST.getlist('mockup_pks')

    # little check
    if _mockup_pks:

        # Check that all values are integers.
        _valid_pk_list = set()
        # ..
        for _pk in _mockup_pks:
            try:
                int(_pk)
            except (TypeError, ValueError):
                continue
            else:
                _valid_pk_list.add(_pk)

        # Delete all the messages, if they belong to the user.
        _changed_list = set()
        # ..
        for _pk in _valid_pk_list:
            # get mockup
            _mockup = get_object_or_404(Mockup, pk=_pk)
            # Check if the user is the owner
            if _mockup.owner == request.user:
                if undo is True:
                    _mockup.deleted_at = None
                else:
                    _mockup.deleted_at = datetime.now()
                # db update
                _mockup.save()
                # result update
                _changed_list.add(_mockup.pk)

        # result message
        if len(_changed_list) != 0: # userena_settings.USERENA_USE_MESSAGES
            if undo:
                _msg = ungettext('Mockup is succesfully restored.',
                                 'Mockups are succesfully restored.',
                                 len(_changed_list))
            else:
                _msg = ungettext('Mockup is successfully removed.',
                                 'Mockups are successfully removed.',
                                 len(_changed_list))
            # ...
            messages.success(request, _msg, fail_silently=True)

    # get next page
    _redirect_to = request.REQUEST.get('next', False)
    # redirect issue
    if _redirect_to:
        return redirect(_redirect_to)
    # default return the list
    else:
        return redirect(reverse('openmockup_list'))
