from django.dispatch import Signal
from notifications import notify

""" Register new signal """
addActivity = Signal()
addedActivity = Signal()
messageSignal = Signal()
postCast = Signal()
postExpire = Signal()


def add_activity(sender, recipient, text, action, arguments=None, game=None, **kwargs):
    """ Simplified addActivity signal.
    """
    addActivity.send(sender=None,
                     user_from=sender,
                     user_to=recipient,
                     action=action,
                     message=text,
                     arguments=arguments,
                     game=game
    )

    if 'to' in arguments.keys():
        arguments['to'] = 'you'

    notify_message = text.format(**arguments)
    notify.send(sender=sender.user, recipient=recipient.user, verb=notify_message)


