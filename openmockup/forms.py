
# django import
from django import forms
from django.utils.translation import ugettext_lazy as _

# wanted import
from openmockup.models import Mockup


class ComposeForm(forms.Form):

    content = forms.CharField(label=_("Content"),
                           widget=forms.Textarea({'class': 'wanted-descr'}),
                           required=True)

    def save(self, owner, mockup=None):
        # parser request
        _content = self.cleaned_data['content']
        # do save
        mockup = Mockup(owner=owner)\
                if mockup is None else mockup
        # update content
        mockup.content = _content
        # save
        mockup.save()
        # return it
        return mockup
