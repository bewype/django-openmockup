
# django import
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# openmockup import
from openmockup.models import Mockup


class MockupAdmin(admin.ModelAdmin):
    """ Admin announcement class with inline recipients
    """

    fieldsets = (
        (None, {
            'fields': (
                'owner', 'content',
            ),
            'classes': ('monospace' ),
        }),
        (_('Date/time'), {
            'fields': (
                'deleted_at',
            ),
            'classes': ('collapse', 'wide'),
        }),
    )
    list_display = ('owner', 'content', 'created_at')
    list_filter = ('owner', 'created_at')
    search_fields = ('content',)


admin.site.register(Mockup, MockupAdmin)
