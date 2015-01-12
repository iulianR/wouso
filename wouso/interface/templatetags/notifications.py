from django import template
from core.user.models import Player

register = template.Library()

@register.simple_tag()
def notifications(user):
    html = ""
    player = Player.objects.get(user=user)
    for n in user.notifications.all():
        notification = player.full_name + n.verb + n.timesince()
        html += '<p>' + notification + '</p>'

    return html
