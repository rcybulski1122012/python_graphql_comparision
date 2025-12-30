from typing import Any

from django import forms
from django.core.validators import RegexValidator
from django.db import models
from django.forms import Field as FormField
from django.forms.fields import ChoiceField
from django.utils.translation import gettext_lazy as _


class HexColorField(models.CharField):
    hex_regex = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("max_length", 7)

        super().__init__(*args, **kwargs)

        self.validators.append(
            RegexValidator(
                regex=self.hex_regex,
                message=_("Enter a valid hex color, e.g. #FF0000 or #F00"),
                code="invalid_hex_color",
            ),
        )

    def formfield(
        self,
        form_class: type[FormField] | None = None,
        choices_form_class: type[ChoiceField] | None = None,
        **kwargs: Any,
    ) -> FormField | None:
        defaults = {"widget": forms.TextInput(attrs={"type": "color"})}
        defaults.update(kwargs)
        return super().formfield(
            form_class=form_class,
            choices_form_class=choices_form_class,
            **defaults,
        )
