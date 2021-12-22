from django import template

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.filter
def getvalue(instance, key):    
    return getattr(instance, key, None)