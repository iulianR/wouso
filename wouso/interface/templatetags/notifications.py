from django import template
from core.user.models import Player

register = template.Library()


@register.simple_tag()
def notifications(user):
    html = ""
    recipient = Player.objects.get(user=user)
    for n in user.notifications.all():
        sender = Player.objects.get(user__id=n.actor_object_id)
        # If there is no sender, the message should not contain any user's name
        # E.g. You have earned an achievement
        if sender == recipient:
            notification = 'You ' + n.verb + ' ' + n.timesince() + ' ago.'
        # If a sender exists, create the corresponding message
        # <Sender full name> cast Blind on you
        else:
            name = sender.full_name or sender.user.username
            notification = name + ' ' + n.verb + ' ' + 'you ' + n.timesince() \
                           + ' ago.'
        html += '<p>' + notification + '</p>'

    if html == '':
        html = '<p>You have no notifications yet.'

    return html
