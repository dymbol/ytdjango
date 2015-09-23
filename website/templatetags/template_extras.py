__author__ = '212429133'
#wymagane w celu dodania custowmoej klasy do pola input, select etc w formie
from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})