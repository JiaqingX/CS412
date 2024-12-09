from django import template

register = template.Library()

@register.filter
def in_group(user, group_name):
    """
    检查用户是否属于指定组。
    """
    return user.groups.filter(name=group_name).exists()
