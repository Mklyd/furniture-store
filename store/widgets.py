from django.forms.widgets import CheckboxSelectMultiple
from django.utils.html import format_html
from .models import Image

class ImageSelectMultiple(CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        if hasattr(self, 'choices'):
            for option_value, option_label in self.choices:
                try:
                    image = Image.objects.get(pk=option_value)
                    output = output.replace(f'value="{option_value}"', f'value="{option_value}" data-image-url="{image.image.url}"')
                except Image.DoesNotExist:
                    pass
        return format_html(output)

class ImagePreviewWidget(ClearableFileInput):
    template_with_initial = '<div class="image-preview"><img src="{}" style="max-width: 300px; max-height: 300px;"></div>{}'
    
    def render(self, name, value, attrs=None, renderer=None):
        output = super().render(name, value, attrs, renderer)
        if value and hasattr(value, "url"):
            output = self.template_with_initial.format(value.url, output)
        elif 'data-image-url' in attrs:
            output = self.template_with_initial.format(attrs['data-image-url'], output)
        return format_html(output)
