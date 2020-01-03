""".. Ignore pydocstyle D400.

===========
Core models
===========

.. autoclass:: rolca.core.models.Contest
    :members:

.. autoclass:: rolca.core.models.Theme
    :members:

.. autoclass:: rolca.core.models.Author
    :members:

.. autoclass:: rolca.core.models.Submission
    :members:

.. autoclass:: rolca.core.models.File
    :members:

"""
import hashlib
import io
import os

from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """Base model for all other models."""

    class Meta:
        """BaseModel Meta options."""

        abstract = True

    #: user who created the object
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE
    )

    #: date when the object was created
    created = models.DateTimeField(auto_now_add=True)

    #: date when the object was last modified
    modified = models.DateTimeField(auto_now=True)


class Contest(BaseModel):
    """Model for storing contests.

    Contest object is the main object of single contest. It can contain
    multiple themes and all important dates for contest (start, end and
    results date).
    """

    class Meta:
        """Contest Meta options."""

        verbose_name = _('contest')
        verbose_name_plural = _('contests')

    #: title of the contest
    title = models.CharField(_('Title'), max_length=100)

    #: description of the contest
    description = models.TextField(_('Description'), null=True, blank=True)

    #: date when contest starts
    start_date = models.DateTimeField(_('Start date'))

    #: date when contest ends
    end_date = models.DateTimeField(_('End date'),)

    #: date when results will be published
    publish_date = models.DateTimeField(_('Publish date'), blank=True)

    #: indicate if user must be logged-in to participate in contest
    login_required = models.BooleanField(_('Login required'), default=False)

    def save(self, *args, **kwargs):
        """Save Contest instance."""
        if not self.publish_date:
            self.publish_date = self.end_date

        super().save(*args, **kwargs)

    def __str__(self):
        """Return Contest's title."""
        return self.title

    def is_active(self):
        """Check if contest is active."""
        return self.start_date <= timezone.now() <= self.end_date

    is_active.admin_order_field = 'end_date'
    is_active.boolean = True
    is_active.short_description = _('active')

    def number_of_photos(self):
        """Return number of photos submitted to the current contest."""
        return Submission.objects.filter(theme__contest=self).count()

    number_of_photos.short_description = _('number of submissons')


class Theme(BaseModel):
    """Model for storing themes."""

    class Meta:
        """Theme Meta options."""

        verbose_name = _('theme')
        verbose_name_plural = _('themes')

    #: title of the theme
    title = models.CharField(_('Title'), max_length=100)

    #: contest that theme belongs to
    contest = models.ForeignKey(
        Contest, related_name='themes', on_delete=models.CASCADE
    )

    #: indicates whether the theme is a series or not
    is_series = models.BooleanField(default=False)

    #: number of photos that can be submited to theme
    n_photos = models.IntegerField(_('Number of photos'))

    def save(self, *args, **kwargs):
        """Save Theme instance."""
        if getattr(self, 'user', None) is None:
            self.user = self.contest.user

        super(Theme, self).save(*args, **kwargs)

    def __str__(self):
        """Return theme's title."""
        return self.title


def _generate_filename(instance, filename, prefix):
    """Generate unique filename with given prefix."""
    md5 = hashlib.md5()
    for chunk in instance.file.chunks():
        md5.update(chunk)
    extension = os.path.splitext(filename)[1]
    return os.path.join(prefix, md5.hexdigest() + extension)


def generate_file_filename(instance, filename):
    """Generate filename for uploaded photo."""
    return _generate_filename(instance, filename, 'photos')


def generate_thumb_filename(instance, filename):
    """Generate filename for thumbnails of uploaded photos."""
    return _generate_filename(instance, filename, 'thumbs')


class Submission(BaseModel):
    """Model for storing uploaded submissions."""

    class Meta:
        """Submission Meta options."""

        verbose_name = _('submission')
        verbose_name_plural = _('submissions')

    title = models.CharField(_('Title'), max_length=100, null=True, blank=True)

    author = models.ForeignKey('Author', on_delete=models.CASCADE)

    theme = models.ForeignKey(Theme, on_delete=models.PROTECT)

    photo = models.OneToOneField('File', on_delete=models.CASCADE)

    def __str__(self):
        """Return string representation of Submission object."""
        return self.title


class File(BaseModel):
    """Model for storing uploaded images.

    Uploaded images can be stored prior to creating Submission
    instance. This way you can upload images while user is typing other
    data.Images are checked if meet size and format requirements before
    saving.

    """

    class Meta:
        """File Meta options."""

        verbose_name = _('file')
        verbose_name_plural = _('files')

    #: uploaded file
    file = models.ImageField(upload_to=generate_file_filename)

    #: thumbnail of uploaded file
    thumbnail = models.ImageField(upload_to=generate_thumb_filename)

    def save(self, *args, **kwargs):
        """Add photo thumbnail and save object."""
        if not self.pk:  # on create
            image = Image.open(self.file)
            image.thumbnail((100, 100), Image.ANTIALIAS)

            thumb = io.BytesIO()
            image.save(
                thumb, format="jpeg", quality=100, optimize=True, progressive=True
            )
            self.thumbnail = InMemoryUploadedFile(
                thumb, None, self.file.name, 'image/jpeg', thumb.tell(), None
            )

        super(File, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Delete attached images and actual object."""
        self.file.delete(save=False)
        self.thumbnail.delete(save=False)

        super(File, self).delete(*args, **kwargs)

    def get_long_edge(self):
        """Return longer edge of the image."""
        return max(self.file.width, self.file.height)

    def __str__(self):
        """Return string representation of File object."""
        submission = self.submission_set.first()
        submission_title = submission.title if submission else '?'
        submission_id = submission.pk if submission else '?'
        return "id: {}, filename: {}, submission id: {}, submission title: {}".format(
            self.pk, self.file.name, submission_id, submission_title
        )


class Author(BaseModel):
    """Model for storing participents."""

    class Meta:
        """Author Meta options."""

        verbose_name = _('author')
        verbose_name_plural = _('authors')

    #: ``Author``'s first name
    first_name = models.CharField(_('First name'), max_length=30)

    #: ``Author``'s last name
    last_name = models.CharField(_('Last name'), max_length=30)

    #: ``Author``'s email
    email = models.EmailField(_('Email'), null=True, blank=True)

    #: mentor
    mentor = models.CharField(_('Mentor'), max_length=60, null=True, blank=True)

    def __str__(self):
        """Return string representation of Author object."""
        return "{} {}".format(self.first_name, self.last_name)
