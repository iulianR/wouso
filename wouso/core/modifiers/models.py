from django.db import models
from django.conf import settings


class Modifier(models.Model):
    """ Basic model for all the magic.
    It is extended by:
        - Artifacts
        - Spell scrolls
        - Skills
        - Badges
        - Achievements
    """

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000, null=True, blank=True)
    #icon = models.ImageField(upload_to=settings.MEDIA_ARTIFACTS_DIR, blank=True, null=True)
    type = models.CharField(max_length=100)
    available = models.BooleanField(default=True)
    #constraints = models.CommaSeparatedIntegerField
    #effects =