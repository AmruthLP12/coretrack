from datetime import date
import textwrap
from django import forms
from django.core.validators import RegexValidator
from dal import autocomplete
from django.utils.safestring import mark_safe
from django.core.files.uploadedfile import UploadedFile

# Default Tailwind CSS classes for form fields
DEFAULT_TAILWIND_CLASSES = (
    "w-full px-3 py-2 rounded-lg border border-border bg-surface text-text "
    "placeholder-text-muted shadow-sm transition duration-200 "
    "focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-primary-400 "
    "dark:bg-surface-dark dark:border-border-dark dark:text-text-dark "
    "dark:placeholder-text-muted-dark"
)


def get_tailwind_classes(extra_classes=""):
    """
    Returns the default Tailwind CSS classes with optional extra classes.

    Args:
        extra_classes (str): Additional CSS classes to append.

    Returns:
        str: Combined CSS class string.
    """
    return f"{DEFAULT_TAILWIND_CLASSES} {extra_classes}".strip()


def get_date_field(
    required=True,
    css_class=None,
    placeholder="Select a date",
    max_date=None,
    min_date=None,  # <-- added min_date parameter
    default_date=None,
    **kwargs,
):
    """
    Returns a DateField with Tailwind styling.

    Args:
        required (bool): Whether the field is required.
        css_class (str): CSS class for styling.
        placeholder (str): Placeholder text.
        max_date (str): Maximum date allowed (ISO format or 'today').
        min_date (str): Minimum date allowed (ISO format or 'today').
        **kwargs: Additional field options.

    Returns:
        forms.DateField
    """

    # Use DEFAULT_TAILWIND_CLASSES if no custom class is passed
    base_class = css_class or DEFAULT_TAILWIND_CLASSES
    css_class = f"block {base_class}"
    widget_attrs = {
        "type": "date",
        "placeholder": placeholder,
        "class": css_class,
        "data-toggle": "datepicker",
        "data-date-format": "DD/MM/YYYY",
        "pattern": "[0-9]{2}/[0-9]{2}/[0-9]{4}",
        **kwargs.get("attrs", {}),
    }

    # Handle max date
    if max_date is not None:
        widget_attrs["max"] = (
            date.today().isoformat() if max_date == "today" else max_date
        )

    # Handle min date
    if min_date is not None:
        widget_attrs["min"] = (
            date.today().isoformat() if min_date == "today" else min_date
        )

    # Handle default date (pre-set value)
    if default_date is not None:
        widget_attrs["value"] = (
            default_date.isoformat()
            if hasattr(default_date, "isoformat")
            else default_date
        )

    return forms.DateField(
        widget=forms.DateInput(attrs=widget_attrs),
        required=required,
        label=kwargs.get("label"),
        help_text=kwargs.get("help_text"),
        **kwargs.get("field_kwargs", {}),
    )


def get_date_time_field(
    required=True,
    css_class=None,
    placeholder="Select a date and time",
    max_date=None,
    min_date=None,  # <-- added min_date parameter
    default_date=None,
    **kwargs,
):
    """
    Select a date and time.

    Args:
        required (bool): Whether the field is required.
        css_class (str): CSS class for styling.
        placeholder (str): Placeholder text.
        max_date (str): Maximum date allowed (ISO format or 'today').
        min_date (str): Minimum date allowed (ISO format or 'today').
        **kwargs: Additional field options.

    Returns:
        forms.DateField: Configured date field.
    """

    # Use DEFAULT_TAILWIND_CLASSES if no custom class is passed
    base_class = css_class or DEFAULT_TAILWIND_CLASSES
    css_class = f"block {base_class}"

    widget_attrs = {
        "type": "datetime-local",
        "placeholder": placeholder,
        "class": css_class,
        "data-toggle": "datetimepicker",
        "data-date-format": "DD/MM/YYYY HH:mm",
        "pattern": "[0-9]{2}/[0-9]{2}/[0-9]{4} [0-9]{2}:[0-9]{2}",
        **kwargs.get("attrs", {}),
    }

    # Handle max date
    if max_date is not None:
        widget_attrs["max"] = (
            date.today().isoformat() if max_date == "today" else max_date
        )

    # Handle min date
    if min_date is not None:
        widget_attrs["min"] = (
            date.today().isoformat() if min_date == "today" else min_date
        )

    # Handle default date (pre-set value)
    if default_date is not None:
        widget_attrs["value"] = (
            default_date.isoformat()
            if hasattr(default_date, "isoformat")
            else default_date
        )

    return forms.DateTimeField(
        widget=forms.DateTimeInput(attrs=widget_attrs),
        required=required,
        label=kwargs.get("label"),
        help_text=kwargs.get("help_text"),
        **kwargs.get("field_kwargs", {}),
    )   

def get_phone_field(
    placeholder="e.g., 9876543210 or +91 9876543210",
    css_class=None,
    error_message="Enter a valid Indian phone number (e.g., +919876543210 or 9876543210).",
    regex=r"^(?:\+91)?[6-9]\d{9}$",
    required=False,
    default_date=None,
    **kwargs,
):
    """
    Returns a CharField with regex validation for Indian phone numbers.

    Args:
        placeholder (str): Placeholder text for the input field.
        css_class (str): CSS classes for Tailwind styling.
        error_message (str): Error message for invalid phone numbers.
        regex (str): Regex pattern for phone validation.
        **kwargs: Additional widget attributes or field kwargs.

    Returns:
        forms.CharField: Configured phone field with regex validation.
    """

    # Use DEFAULT_TAILWIND_CLASSES if no custom class is passed
    base_class = css_class or DEFAULT_TAILWIND_CLASSES
    css_class = f"block {base_class}"
    phone_regex = RegexValidator(
        regex=regex,
        message=error_message,
    )

    widget_attrs = {
        "class": css_class,
        "placeholder": placeholder,
        **kwargs.get("attrs", {}),
    }

    return forms.CharField(
        validators=[phone_regex],
        widget=forms.TextInput(attrs=widget_attrs),
        max_length=13,  # +91 and 10 digits
        help_text=kwargs.get("help_text"),
        required=required,
        **kwargs.get("field_kwargs", {}),
    )


def get_text_field(
    placeholder="",
    required=False,
    css_class=DEFAULT_TAILWIND_CLASSES,
    max_length=None,
    disabled=False,
    **kwargs,
):
    """
    Returns a CharField for text-based inputs (e.g., name, email).

    Args:
        placeholder (str): Placeholder text.
        css_class (str): CSS classes for styling.
        max_length (int): Maximum length of the field.
        **kwargs: Additional widget attributes or field kwargs.

    Returns:
        forms.CharField: Configured text field.
    """
    widget_attrs = {
        "class": get_tailwind_classes(kwargs.get("extra_classes", ""))
        if css_class == DEFAULT_TAILWIND_CLASSES
        else css_class,
        "placeholder": placeholder,
        **kwargs.get("attrs", {}),
    }

    return forms.CharField(
        widget=forms.TextInput(attrs=widget_attrs),
        max_length=max_length,
        required=required,
        help_text=kwargs.get("help_text"),
        label=kwargs.get("label"),
        disabled=disabled,
        **kwargs.get("field_kwargs", {}),
    )


def get_textarea_field(
    placeholder="", required=True, css_class=DEFAULT_TAILWIND_CLASSES, rows=3, **kwargs
):
    """
    Returns a CharField for textarea inputs.

    Args:
        placeholder (str): Placeholder text.
        css_class (str): CSS classes for styling.
        rows (int): Number of rows for the textarea.
        **kwargs: Additional widget attributes or field kwargs.

    Returns:
        forms.CharField: Configured textarea field.
    """
    widget_attrs = {
        "class": get_tailwind_classes(kwargs.get("extra_classes", "resize-y"))
        if css_class == DEFAULT_TAILWIND_CLASSES
        else css_class,
        "placeholder": placeholder,
        "rows": rows,
        
        **kwargs.get("attrs", {}),
    }

    field = forms.CharField(
        widget=forms.Textarea(attrs=widget_attrs),
        required=required,
        help_text=kwargs.get("help_text"),
        label=kwargs.get("label"),
        strip=True,           # ← already good
        **kwargs.get("field_kwargs", {}),
    )

    # Optional: force clean initial value
    if 'initial' in kwargs and isinstance(kwargs['initial'], str):
    # Remove common indentation, then strip outer whitespace
        cleaned = textwrap.dedent(kwargs['initial']).strip()
        field.initial = cleaned if cleaned else None
    return field


def get_email_field(
    placeholder="Enter email address",
    required=True,
    css_class=DEFAULT_TAILWIND_CLASSES,
    **kwargs,
):
    """
    Returns an EmailField for email inputs.
    """
    widget_attrs = {
        "class": get_tailwind_classes(kwargs.get("extra_classes", ""))
        if css_class == DEFAULT_TAILWIND_CLASSES
        else css_class,
        "placeholder": placeholder,
        "required": required,
        **kwargs.get("attrs", {}),
    }

    return forms.EmailField(
        widget=forms.EmailInput(attrs=widget_attrs),
        help_text=kwargs.get("help_text"),
        **kwargs.get("field_kwargs", {}),
        required=required,
    )


def get_select_field(css_class=DEFAULT_TAILWIND_CLASSES, **kwargs):
    """
    Returns a ChoiceField or ModelChoiceField for select inputs.
    """
    widget_attrs = {
        "class": get_tailwind_classes(kwargs.get("extra_classes", ""))
        if css_class == DEFAULT_TAILWIND_CLASSES
        else css_class,
        **kwargs.get("attrs", {}),
    }

    return forms.ChoiceField(
        widget=forms.Select(attrs=widget_attrs),
        help_text=kwargs.get("help_text"),
        **kwargs.get("field_kwargs", {}),
    )


def get_choice_field(
    choices,
    required=True,
    css_class=DEFAULT_TAILWIND_CLASSES,
    placeholder="Select an option",
    **kwargs,
):
    """
    Returns a ChoiceField for select inputs.

    Args:
        choices (list or tuple): List/tuple of (value, label) pairs.
        required (bool): Whether the field is required.
        css_class (str): CSS classes for styling.
        placeholder (str): Placeholder text (added as an empty option).
        **kwargs: Additional widget attributes or field kwargs.

    Returns:
        forms.ChoiceField: Configured select field.
    """
    widget_attrs = {
        "class": get_tailwind_classes(kwargs.get("extra_classes", ""))
        if css_class == DEFAULT_TAILWIND_CLASSES
        else css_class,
        **kwargs.get("attrs", {}),
    }

    final_choices = [("", placeholder)] + list(choices)

    return forms.ChoiceField(
        label=kwargs.get("label"),
        help_text=kwargs.get("help_text"),
        choices=final_choices,
        widget=forms.Select(attrs=widget_attrs),
        required=required,
        initial=kwargs.get("initial"),
        **kwargs.get("field_kwargs", {}),
    )


def get_foreign_key_field(
    queryset,
    placeholder="Select an option",
    required=True,
    css_class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500",
    extra_attrs=None,
    **kwargs,
):
    """
    Returns a plain ModelChoiceField with a Select widget (no JS).
    """
    attrs = {
        "class": css_class,
    }
    if extra_attrs:
        attrs.update(extra_attrs)

    # Placeholder support (only for non-required fields)
    if not required:
        empty_label = placeholder
    else:
        empty_label = None

    return forms.ModelChoiceField(
        queryset=queryset,
        widget=forms.Select(attrs=attrs),
        required=required,
        help_text=kwargs.get("help_text"),
        label=kwargs.get("label"),
        empty_label=empty_label,
    )


def get_number_field(
    placeholder="", required=True, css_class=DEFAULT_TAILWIND_CLASSES, **kwargs
):
    """
    Returns a NumberField for numeric inputs.

    Args:
        placeholder (str): Placeholder text.
        css_class (str): CSS classes for styling.
        **kwargs: Additional widget attributes or field kwargs.

    Returns:
        forms.IntegerField: Configured number field.
    """
    widget_attrs = {
        "class": get_tailwind_classes(kwargs.get("extra_classes", ""))
        if css_class == DEFAULT_TAILWIND_CLASSES
        else css_class,
        "step": "0.01",
        "placeholder": placeholder,
        "help_text": kwargs.get("help_text"),
        **kwargs.get("attrs", {}),
    }

    return forms.DecimalField(
        widget=forms.NumberInput(attrs=widget_attrs),
        required=required,
        label=kwargs.get("label"),
        help_text=kwargs.get("help_text"),
        **kwargs.get("field_kwargs", {}),
    )


def get_model_select2_field(
    queryset,
    autocomplete_url,
    placeholder="Select an option",
    required=True,
    css_class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500",
    extra_attrs=None,
    minimum_input_length=0,
):
    """
    Returns a ModelChoiceField with a ModelSelect2 widget for autocomplete functionality.

    Args:
        queryset: The queryset for the ModelChoiceField (e.g., Department.objects.all()).
        autocomplete_url: The URL name for the autocomplete view (e.g., "department_autocomplete").
        placeholder: The placeholder text for the select field (default: "Select an option").
        required: Whether the field is required (default: True).
        css_class: CSS classes for the widget (default: Tailwind classes).
        extra_attrs: Additional widget attributes (default: None).
        minimum_input_length: Minimum input length for autocomplete (default: 0).

    Returns:
        A forms.ModelChoiceField instance with a ModelSelect2 widget.
    """
    attrs = {
        "class": css_class,
        "data-placeholder": placeholder,
    }
    if minimum_input_length > 0:
        attrs["data-minimum-input-length"] = minimum_input_length
    if extra_attrs:
        attrs.update(extra_attrs)

    return forms.ModelChoiceField(
        queryset=queryset,
        widget=autocomplete.ModelSelect2(
            url=autocomplete_url,
            attrs=attrs,
        ),
        required=required,
    )


def get_forwarding_model_select2_field(
    queryset,
    autocomplete_url,
    forward_fields,
    placeholder="Select an option",
    required=True,
    css_class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500",
    extra_attrs=None,
    minimum_input_length=0,
    **kwargs,
):
    """
    Returns a ModelChoiceField with a ModelSelect2 widget and forwarding functionality.

    Args:
        queryset: The queryset for the ModelChoiceField.
        autocomplete_url: The URL name for the autocomplete view.
        forward_fields: List of fields to forward for dynamic filtering (e.g., ["pay_level"]).
        placeholder: Placeholder text.
        required: Whether the field is required.
        css_class: CSS classes for the widget.
        extra_attrs: Additional HTML attributes for the widget.
        minimum_input_length: Minimum input length before triggering autocomplete.

    Returns:
        A forms.ModelChoiceField instance with a forwarding ModelSelect2 widget.
    """
    attrs = {
        "class": css_class,
        "data-placeholder": placeholder,
    }
    if minimum_input_length > 0:
        attrs["data-minimum-input-length"] = minimum_input_length
    if extra_attrs:
        attrs.update(extra_attrs)

    return forms.ModelChoiceField(
        queryset=queryset,
        widget=autocomplete.ModelSelect2(
            url=autocomplete_url,
            forward=forward_fields,
            attrs=attrs,
        ),
        help_text=kwargs.get("help_text"),
        required=required,
    )


def get_model_select_field(
    queryset,
    placeholder="Select an option",
    required=True,
    css_class=None,
    extra_attrs=None,
    to_field_name=None,
    **kwargs,
):
    """
    Returns a ModelChoiceField using your Tailwind theme + Select2 support.
    """

    # If custom class not passed → attach Tailwind classes + select2 classes
    final_css = css_class or ("select2 sc " + get_tailwind_classes())

    attrs = {
        "class": final_css,
        "data-placeholder": placeholder,
    }

    if extra_attrs:
        attrs.update(extra_attrs)

    field_kwargs = {
        "queryset": queryset,
        "widget": forms.Select(attrs=attrs),
        "required": required,
        "help_text": kwargs.get("help_text"),
        "label": kwargs.get("label"),
    }

    if to_field_name:
        field_kwargs["to_field_name"] = to_field_name

    return forms.ModelChoiceField(**field_kwargs)


def get_date_select_field(
    date_list,
    placeholder="Select a date",
    required=True,
    css_class=None,
    extra_attrs=None,
    **kwargs,
):
    """
    Returns a ChoiceField specifically for dates or simple choices.
    """
    # Use DEFAULT_TAILWIND_CLASSES if no custom class is passed
    base_class = css_class or DEFAULT_TAILWIND_CLASSES

    attrs = {
        "class": f"select2 {base_class}",
        "data-placeholder": placeholder,
    }

    if extra_attrs:
        attrs.update(extra_attrs)

    choices = [(d, d.strftime("%d-%m-%Y")) for d in date_list]

    return forms.ChoiceField(
        choices=choices,
        required=required,
        widget=forms.Select(attrs=attrs),
        label=kwargs.get("label"),
        help_text=kwargs.get("help_text"),
    )


def get_model_select_multiple_field(
    queryset,
    placeholder="Select options",
    required=False,
    css_class=None,
    extra_attrs=None,
    **kwargs,
):
    """
    Returns a ModelMultipleChoiceField with a SelectMultiple widget for multi-select functionality.

    Args:
        queryset: The queryset for the ModelMultipleChoiceField (e.g.,  SalaryCategory.objects.filter(is_active=True)).
        placeholder: The placeholder text for the select field (default: "Select options").
        required: Whether the field is required (default: True).
        css_class: CSS classes for the widget (default: Tailwind classes with select2).
        extra_attrs: Additional widget attributes (default: None).

    Returns:
        A forms.ModelMultipleChoiceField instance with a SelectMultiple widget.
    """

    # Use DEFAULT_TAILWIND_CLASSES if no custom class is passed
    base_class = css_class or DEFAULT_TAILWIND_CLASSES
    css_class = f"select2 {base_class}"

    attrs = {
        "class": css_class,
        "data-placeholder": placeholder,
    }
    if extra_attrs:
        attrs.update(extra_attrs)

    return forms.ModelMultipleChoiceField(
        queryset=queryset,
        widget=forms.SelectMultiple(
            attrs=attrs,
        ),
        help_text=kwargs.get("help_text"),
        required=required,
    )


def get_checkbox_multiple_field(
    queryset, required=False, label=None, help_text=None, initial=None
):
    """
    Returns a ModelMultipleChoiceField rendered as nicely styled Tailwind checkboxes.
    """
    return forms.ModelMultipleChoiceField(
        queryset=queryset,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "space-y-2",  # adds vertical spacing between items
            }
        ),
        required=required,
        label=label,
        help_text=help_text,
        initial=initial,
    )


def get_checkbox_field_multiple_field(
    queryset,
    name_field,
    required=False,
    label=None,
    help_text=None,
):
    """
    Create a MultipleChoiceField with choices based on the specified name_field.
    Queryset is always refreshed when the form is created.
    """

    # If queryset was passed directly (e.g., Department.objects.all()),
    # turn it into a callable so it refreshes each time.
    queryset_func = queryset if callable(queryset) else (lambda: queryset.all())

    # Build choices fresh every time
    objects = queryset_func()
    choices = [(getattr(obj, name_field), getattr(obj, name_field)) for obj in objects]
    initial_values = [value for value, _ in choices]

    return forms.MultipleChoiceField(
        choices=choices,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "form-checkbox h-5 w-5 text-blue-600 rounded focus:ring-blue-500 border-gray-300",
                "container_class": "border border-gray-300 rounded-lg overflow-hidden",
                "item_class": "flex items-center p-3 border-b border-gray-200 hover:bg-gray-50",
                "label_class": "ml-3 text-sm text-gray-700",
            }
        ),
        required=required,
        label=label,
        help_text=help_text,
        initial=initial_values,
    )


def get_year_choice_field(
    past_years=5,
    future_years=2,
    label="Year",
    required=False,
    css_class="select2 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500",
    extra_attrs=None,
    initial=None,
    **kwargs,
):
    """
    Returns a ChoiceField for selecting a year.
    Default range: last 5 years + current year + next 2 years.
    """

    current_year = date.today().year

    if initial is None:
        initial = current_year

    start_year = current_year - past_years
    end_year = current_year + future_years

    choices = [("", f"Select {label}")] + [
        (str(y), str(y)) for y in range(start_year, end_year + 1)
    ]

    attrs = {
        "class": css_class,
        "data-placeholder": f"Select {label}",
    }

    if extra_attrs:
        attrs.update(extra_attrs)

    return forms.ChoiceField(
        choices=choices,
        label=label,
        required=required,
        help_text=kwargs.get("help_text"),
        widget=forms.Select(attrs=attrs),
        initial=str(initial),
    )

def get_month_choice_field(
    label="Month",
    required=False,
    css_class="select2 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500",
    extra_attrs=None,
    initial=None,
    **kwargs,
):
    """
    Returns a ChoiceField for selecting a month (January to December).

    Args:
        label: The field label (default: "Month").
        required: Whether the field is required (default: False).
        css_class: CSS classes for the widget (default: Tailwind classes).
        extra_attrs: Additional widget attributes (default: None).

    Returns:
        A forms.ChoiceField instance with a Select widget.
    """
    choices = [
        ("", f"Select {label}"),
        ("1", "January"),
        ("2", "February"),
        ("3", "March"),
        ("4", "April"),
        ("5", "May"),
        ("6", "June"),
        ("7", "July"),
        ("8", "August"),
        ("9", "September"),
        ("10", "October"),
        ("11", "November"),
        ("12", "December"),
    ]
    attrs = {
        "class": css_class,
        "data-placeholder": f"Select {label}",
    }
    if extra_attrs:
        attrs.update(extra_attrs)

    return forms.ChoiceField(
        choices=choices,
        label=label,
        required=required,
        help_text=kwargs.get("help_text"),
        widget=forms.Select(attrs=attrs),
        initial=initial,
    )


def get_financial_year_choice_field(
    label="Financial Year",
    required=False,
    css_class="select2 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500",
    extra_attrs=None,
    **kwargs,
):
    """
    Returns a ChoiceField for selecting a financial year in the format YYYY-YYYY+1.
    Value submitted is the first year (YYYY).

    Example: "2025-2026" → value="2025"
    """
    from django import forms
    from datetime import date

    # Determine current financial year start
    today = date.today()
    current_year = today.year if today.month >= 4 else today.year - 1

    # Last 5 years (including current)
    start_year = current_year - 4
    end_year = current_year + 1

    choices = [("", f"Select {label}")] + [
        (str(y), f"{y}-{y + 1}") for y in range(start_year, end_year + 1)
    ]

    attrs = {
        "class": css_class,
        "data-placeholder": f"Select {label}",
    }
    if extra_attrs:
        attrs.update(extra_attrs)

    return forms.ChoiceField(
        choices=choices,
        label=label,
        required=required,
        help_text=kwargs.get("help_text"),
        widget=forms.Select(attrs=attrs),
        initial=str(current_year),
    )


def get_toggle_checkbox_field(
    label="Toggle",
    required=False,
    initial=False,
    extra_classes="",
    extra_attrs=None,
    **kwargs,
):
    """
    Returns a BooleanField styled as a custom toggle switch using Tailwind CSS classes.
    """

    # Manual Tailwind-based styling
    default_classes = (
        "toggle border-red-600 bg-red-500 "
        "checked:border-green-500 checked:bg-green-400 checked:text-green-800"
    )

    # Combine classes
    classes = f"{default_classes} {extra_classes}".strip()

    attrs = {
        "class": classes,
        "data-toggle": "switch",
        **(extra_attrs or {}),
    }

    return forms.BooleanField(
        label=label,
        required=required,
        initial=initial,
        help_text=kwargs.get("help_text"),
        widget=forms.CheckboxInput(attrs=attrs),
    )


def get_simple_toggle_field(
    label="Toggle",
    required=False,
    initial=False,
    size="md",  # 'xs', 'sm', 'md', 'lg'
    color="success",  # 'success', 'primary', 'secondary', 'accent', 'info', 'warning', 'error'
    direction="ltr",
    extra_attrs=None,
):
    """
    Returns a BooleanField with predefined DaisyUI toggle styles and sizes.

    Args:
        label: The field label (default: "Toggle").
        required: Whether the field is required (default: False).
        initial: Initial value of the toggle (default: False).
        size: Toggle size - 'xs', 'sm', 'md', 'lg' (default: 'md').
        color: Toggle color theme (default: 'success').
        direction: Sliding direction - 'ltr' or 'rtl' (default: 'ltr').
        extra_attrs: Additional widget attributes (default: None).

    Returns:
        A forms.BooleanField instance with DaisyUI toggle styling.

    Example:
        class PreferenceForm(forms.Form):
            dark_mode = get_simple_toggle_field(
                label="Enable Dark Mode",
                size="lg",
                color="primary",
                direction="rtl"
            )
    """
    # Size configurations
    sizes = {
        "xs": "toggle-xs",
        "sm": "toggle-sm",
        "md": "toggle-md",
        "lg": "toggle-lg",
    }

    size_class = sizes.get(size, sizes["md"])

    return get_toggle_checkbox_field(
        label=label,
        required=required,
        initial=initial,
        css_class=f"toggle {size_class}",
        color=color,
        direction=direction,
        extra_attrs=extra_attrs,
    )


def get_year_choices():
    current_year = date.today().year
    # If we're before April, financial year starts in previous year
    if date.today().month < 4:
        current_year -= 1

    choices = []
    for i in range(10):  # 10 previous years
        start_year = current_year - i
        end_year = start_year + 1
        label = f"{start_year}-{end_year}"
        choices.append((start_year, label))  # <-- FIX: store integer, show label
    return choices


def get_file_upload_field(
    placeholder="Upload File",
    allowed_types=None,  # e.g. ["image/png", "application/pdf"]
    max_size=None,  # size in MB (optional)
    multiple=False,
    css_class=DEFAULT_TAILWIND_CLASSES,  # use your utility class
    **kwargs,
):
    """
    Creates a reusable file input field styled with Tailwind
    and optional validation (file type, size, etc.).
    """

    # --- Widget attributes ---
    widget_attrs = {
        "class": f"{css_class} file:border file:px-3 file:py-2 file:rounded-lg cursor-pointer",
        "placeholder": placeholder,
    }

    if multiple:
        widget_attrs["multiple"] = True

    # --- Django field kwargs ---
    field_kwargs = kwargs.get("field_kwargs", {})
    field_kwargs.update(
        {
            "required": kwargs.get("required", False),
            "label": kwargs.get("label"),
            "help_text": kwargs.get(
                "help_text",
                "Allowed Format: " + ", ".join(allowed_types) if allowed_types else "",
            ),
        }
    )

    # --- Create Field ---
    field = forms.FileField(
        widget=forms.ClearableFileInput(attrs=widget_attrs),
        **field_kwargs,
    )

    # === Optional Validation ===
    original_clean = field.clean  # preserve original

    def clean_uploaded_file(value, initial=None):
        file = original_clean(value, initial)

        if not file:
            return file

        if isinstance(file, UploadedFile):

            if allowed_types and file.content_type not in allowed_types:
                raise forms.ValidationError(
                    f"Invalid file type: {file.content_type}. Allowed: {', '.join(allowed_types)}"
                )

            if max_size and file.size > max_size * 1024 * 1024:
                raise forms.ValidationError(f"File size exceeds {max_size}MB limit.")

        return file

    field.clean = clean_uploaded_file

    return field
 