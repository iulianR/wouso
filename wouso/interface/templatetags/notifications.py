from django import template

register = template.Library()

@register.simple_tag()
def notifications(user):
    html = ""
    for n in user.notifications.all():
        html += '<p>' + str(n) + '</p>'
    return html
