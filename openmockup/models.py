
# django db
from django.db import models
# django contrib
from django.contrib.auth.models import User
# django utils
from django.utils.text import truncate_words
from django.utils.translation import ugettext_lazy as _


class Mockup(models.Model):
    """ Private mockup model, from user to user(s)
    """

    owner = models.ForeignKey(User, related_name="mockups",
            verbose_name=_("owner"))
    content = models.TextField(_("content"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    deleted_at = models.DateTimeField(_("deleted at"), null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("mockup")
        verbose_name_plural = _("mockups")

    def __unicode__(self):
        """ Human representation, displaying first ten words of the
        content.
        """
        return truncate_words(self.content, 10)

    @models.permalink
    def get_absolute_url(self):
        return ("openmockup_detail", None,\
                {"mockup_id": self.pk})
