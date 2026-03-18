from django import forms
from .models import Tracker
from theme.utils import input_fields_utils


TRACKER_FIELDS = [
    {
        "name": "title",
        "label": "Title",
        "type": "text",
        "required": True,
    },
    {
        "name": "description",
        "label": "Description",
        "type": "textarea",
    },
    {
        "name": "amount",
        "label": "Amount",
        "type": "number",
    },
    {
        "name": "priority",
        "label": "Priority",
        "type": "select",
        "choices": [("low", "Low"), ("medium", "Medium"), ("high", "High")],
    },
]


class TrackerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        dynamic_fields = kwargs.pop("dynamic_fields", [])
        super().__init__(*args, **kwargs)

        # Add dynamic fields
        for field in dynamic_fields:
            name = field["name"]
            field_type = field.get("type", "text")
            label = field.get("label", name.capitalize())
            required = field.get("required", False)
            placeholder = field.get("placeholder", f"Enter {label.lower()}...")

            if field_type == "text":
                self.fields[name] = input_fields_utils.get_text_field(
                    label=label,
                    required=required,
                    placeholder=placeholder
                )

            elif field_type == "number":
                self.fields[name] = input_fields_utils.get_number_field(
                    label=label,
                    required=required,
                    placeholder=placeholder
                )

            elif field_type == "textarea":
                self.fields[name] = input_fields_utils.get_textarea_field(
                    label=label,
                    required=required,
                    placeholder=placeholder
                )

            elif field_type == "select":
                self.fields[name] = input_fields_utils.get_choice_field(
                    choices=field.get("choices", []),
                    label=label,
                    required=required,
                    placeholder=field.get("placeholder", "Select an option")
                )

        # Style the static 'status' field if it exists
        if "status" in self.fields:
            self.fields["status"] = input_fields_utils.get_choice_field(
                choices=Tracker.Status.choices,
                label="Status",
                required=True,
                initial=self.instance.status if self.instance else Tracker.Status.PENDING
            )

        # Pre-fill existing JSON data (edit case)
        if self.instance and self.instance.data:
            for key, value in self.instance.data.items():
                if key in self.fields:
                    self.fields[key].initial = value

    class Meta:
        model = Tracker
        fields = ["status"]  # Only static fields here

    def clean(self):
        cleaned_data = super().clean()

        # Extract dynamic data
        dynamic_data = {}
        for key in self.fields:
            if key not in self.Meta.fields:
                dynamic_data[key] = cleaned_data.get(key)

        cleaned_data["data"] = dynamic_data
        return cleaned_data

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)

        # Save JSON data
        instance.data = self.cleaned_data.get("data", {})

        if user:
            if not instance.pk:
                instance.requested_by = user
            instance.updated_by = user

        if commit:
            instance.save()

        return instance
