from django.template import Library
from django import template

register = Library()

# Increase = New Number - Original Number
# Then:  divide the increase by the original number and multiply the answer by 100.

@register.filter(is_safe=True)
def percent_increase(value, arg):
    try:
        "Divides the value by the arg"
        increase = float(value) - float(arg)
        percentage = (increase / float(value))*100
        # return '{0:.0f}'.format(percentage)
        percentage = '{0:.0f}'.format(percentage)
        percentage = int(percentage)
    except:
        percentage = 0
    return - percentage





