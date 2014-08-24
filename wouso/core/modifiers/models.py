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

    @staticmethod
    def give_to_player(player, modifier, amount=1):
        if amount <= 0:
            return

        try:
            pamount = PlayerModifierAmount.objects.get(player=player, modifier=modifier)
        except PlayerModifierAmount.DoesNotExist:
            pamount = 0

        if not pamount:
            pamount = PlayerModifierAmount.objects.create(player=player, modifier=modifier)
        else:
            pamount.amount += amount
            pamount.save()
        return pamount

    @staticmethod
    def remove_from_player(player, modifier, amount=1):
        if amount <= 0:
            return

        try:
            pamount = PlayerModifierAmount.objects.get(player=player, modifier=modifier)
            assert pamount.amount > 0
        except (PlayerModifierAmount.DoesNotExist, AssertionError):
            return 'Spell unavailable'

        pamount.amount -= amount
        pamount.save()
        return pamount


    def __unicode__(self):
        return self.name


class SpellScroll(Modifier):
    #TYPES = (('o', 'neutral'), ('p', 'positive'), ('n', 'negative'), ('s', 'self'))
    duration = models.IntegerField(default=5)

    def __unicode__(self):
        return self.name


class Artifactz(Modifier):
    def __unicode__(self):
        return self.name


class PlayerModifierAmount(models.Model):
    """
     Tie modifier to collecting user
    """
    class Meta:
        unique_together = ('player', 'modifier')

    player = models.ForeignKey('user.Player')
    modifier = models.ForeignKey(Modifier)
    amount = models.IntegerField(default=1)

    def __unicode__(self):
        return u"%s has %s [%d]" % (self.player, self.modifier, self.amount)


class PlayerModifierDue(models.Model):
    """
     Tie modifier, casting user, duration with the victim player
    """
    class Meta:
        unique_together = ('player', 'modifier')

    player = models.ForeignKey('user.Player')
    modifier = models.ForeignKey(Modifier)
    source = models.ForeignKey('user.Player', related_name='modifier_source')
    due = models.DateTimeField()

    seen = models.BooleanField(default=False, blank=True)

    @staticmethod
    def get_expired(date):
        return PlayerModifierDue.objects.filter(due__lte=date)

    def __unicode__(self):
        return u"%s casted on %s until %s [%s]" % \
               (self.spell, self.player, self.due, self.source)