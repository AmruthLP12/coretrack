from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag("field.html")
def render_field(field, label_icon=None, input_icon=None, id=None, **attrs):
    """
    Renders a form field with optional label and input icons.

    Args:
        field: The Django form field.
        label_icon: Icon class for label area (e.g., 'fas fa-user').
        input_icon: Icon class to appear inside the input (e.g., 'fas fa-key').
        **attrs: Any additional HTML attributes to apply to the field.
    """
    widget_attrs = field.field.widget.attrs.copy()
    if id:
        widget_attrs["id"] = id

    # Add padding if input icon is present
    if input_icon:
        widget_attrs["class"] = widget_attrs.get("class", "") + " pl-10"

    for key, value in attrs.items():
        if key == "class":
            widget_attrs["class"] = widget_attrs.get("class", "") + " " + value
        else:
            widget_attrs[key] = value
    field.field.widget.attrs = widget_attrs

    return {
        "field": field,
        "label_icon": label_icon,
        "input_icon": input_icon,
    }


@register.filter
def getitem(obj, key):
    return obj[key]


@register.filter
def zip(a, b):
    return zip(a, b)


@register.filter
def get_field(form, field_name):
    return form[field_name]
