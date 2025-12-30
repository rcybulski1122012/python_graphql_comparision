from django.db import models
from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class HexColorField(models.CharField):
    hex_regex = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 7)

        super().__init__(*args, **kwargs)

        self.validators.append(RegexValidator(
            regex=self.hex_regex,
            message=_('Enter a valid hex color, e.g. #FF0000 or #F00'),
            code='invalid_hex_color'
        ))

    def formfield(self, **kwargs):
        defaults = {'widget': forms.TextInput(attrs={'type': 'color'})}
        defaults.update(kwargs)
        return super().formfield(**defaults)
