from django import template
register = template.Library()

# getting list elemend by index in template
# {% load index %}
# {{ List|index:0 }}
# {{ List|index:1 }}

@register.filter
def index(List, i):
    return List[int(i)]