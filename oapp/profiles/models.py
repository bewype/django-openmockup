from django.db import models
from django.utils.translation import ugettext_lazy as _

from userena.models import UserenaLanguageBaseProfile

import datetime

class Profile(UserenaLanguageBaseProfile):
    """ Default profile
    """
    website = models.URLField(_('website'), blank=True, verify_exists=True)
    about_me = models.TextField(_('about me'), blank=True)
