from wouso.core import scoring
from wouso.core.user.models import Player
from django.core.management.base import BaseCommand


def exchange(player):
    gold_rate = scoring.calculate('gold-points-rate', gold=1)['points']
    try:
        gold = p.coins['gold'] or 0
    except:
        print 'Invalid amounts'
    else:
        if gold > 0:
            points = gold_rate * gold
            if player.coins['gold'] < gold:
                print 'Insufficient gold'
            else:
                scoring.score(player, None, 'gold-points-rate', gold=gold)
                print 'Converted successfully'
        else:
            print 'No gold to convert'


class Command(BaseCommand):
    def handle_noargs(self, **options):
        for p in Player.objects.all():
            exchange(p)
