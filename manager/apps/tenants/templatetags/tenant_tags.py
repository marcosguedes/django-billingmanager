from django import template

register = template.Library()


@register.inclusion_tag("admin_shortcuts/base.html", takes_context=True)
def admin_shortcuts(context):
    request = context.get("request", None)

    return context
