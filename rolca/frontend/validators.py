"""Rolca_core validators."""
import logging

from PIL import Image

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def _humanize_size(nbytes):
    """Transforn given number of bytes to human readable unit."""
    suffix = None
    for suffix in ['B', 'KB', 'MB', 'GB']:
        if nbytes < 1024:
            break
        nbytes /= 1024

    humanized = '{:.2f}'.format(nbytes).rstrip('0').rstrip('.')
    return '{} {}'.format(humanized, suffix)


def validate_format(value):
    """Check if file is smaller then specified in settings."""
    accepted_formats = getattr(settings, 'ROLCA_ACCEPTED_FORMATS', [])

    if not accepted_formats:
        logger.warning('`validate_format` validation cannot be performed, because '
                       '`ROLCA_ACCEPTED_FORMATS` setting is not defined.')
        return

    if not isinstance(accepted_formats, list):
        msg = '`ROLCA_ACCEPTED_FORMATS` setting must be of type `list`.'
        logger.error(msg)
        raise ImproperlyConfigured(msg)
    image = Image.open(value)

    if image.format not in accepted_formats:
        raise ValidationError('Only following image types are supported: '
                              '{}'.format(', '.join(accepted_formats)))


def validate_size(value):
    """Check if file is smaller then specified in settings."""
    max_size = getattr(settings, 'ROLCA_MAX_SIZE', None)

    if not max_size:
        logger.warning('`validate_size` validation cannot be performed, because '
                       '`ROLCA_MAX_SIZE` setting is not defined.')
        return

    if not isinstance(max_size, int):
        msg = '`ROLCA_MAX_SIZE` setting must be of type `int`.'
        logger.error(msg)
        raise ImproperlyConfigured(msg)

    if value.size > max_size:
        raise ValidationError('Uploaded file must be smaller than '
                              '{}.'.format(_humanize_size(max_size)))


def validate_long_edge(value):
    """Check if file is smaller then specified in settings."""
    max_long_edge = getattr(settings, 'ROLCA_MAX_LONG_EDGE', None)

    if not max_long_edge:
        logger.warning('`validate_long_edge` validation cannot be performed, '
                       'because `ROLCA_MAX_LONG_EDGE` setting is not defined.')
        return

    if not isinstance(max_long_edge, int):
        msg = '`ROLCA_MAX_LONG_EDGE` setting must be of type `int`.'
        logger.error(msg)
        raise ImproperlyConfigured(msg)

    image = Image.open(value)
    if max(image.size) > max_long_edge:
        raise ValidationError('Long edge of the image cannot excede '
                              '{}px.'.format(max_long_edge))
