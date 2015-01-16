from django.dispatch import Signal
from notifications import notify

""" Register new signal """
addActivity = Signal()
addedActivity = Signal()
messageSignal = Signal()
postCast = Signal()
postExpire = Signal()


def add_activity(sender, recipient, message, action, arguments=None, game=None, **kwargs):
    """ Simplified addActivity signal.
    """
    addActivity.send(sender=None,
                     user_from=sender,
                     user_to=recipient,
                     action=action,
                     message=message,
                     arguments=arguments,
                     game=game)

    # Remove user_to from the notification message as notify.send() only needs
    # the verb. The receiving user is saved separately.
    if 'user_to' in arguments:
        arguments.pop('user_to', None)
        message = message.replace(' {user_to}', '')

    notify_message = message.format(**arguments)
    notify.send(sender=sender.user, recipient=recipient.user, verb=notify_message)
