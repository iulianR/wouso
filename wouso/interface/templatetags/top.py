from django import template
from wouso.core.user.models import Race, Player
from django.contrib.auth.decorators import login_required
register = template.Library()


@login_required
@register.inclusion_tag("interface/sidebar/leaderboard.html")
def render_top():
    players = Player.objects.order_by('-points')[:10]

    races = list(Race.objects.exclude(can_play=False))
    races.sort(key=lambda a: a.points, reverse=True)
    races = races[:10]

    return {'top_10_players': players,
            'top_10_races': races}
