"""Rolca_core forms."""
import logging

from django import forms
from django.db import IntegrityError, transaction

from rolca.core.models import File, Photo
from .validators import validate_format, validate_size, validate_long_edge


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class PhotoForm(forms.Form):
    """Form for handling Photo uploads."""

    title = forms.CharField(required=True)
    photo = forms.ImageField(required=True,
                             validators=[validate_format, validate_size, validate_long_edge])

    def save(self, user, author, theme):
        try:
            with transaction.atomic():
                photo_file = File.objects.create(user=user, file=self.cleaned_data['photo'])
                Photo.objects.create(
                    photo=photo_file,
                    user=user,
                    theme=theme,
                    title=self.cleaned_data['title'],
                    author=author,
                )
                logging.info('Saved file')
        except IntegrityError:
            logging.error('Failed to save file')
            raise


ThemeFormSet = forms.formset_factory(PhotoForm, extra=3, max_num=3)
