"""Rolca_core models."""
import hashlib
import io
import os

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from datetime import date
from PIL import Image


class Salon(models.Model):
    """Model for storing salons.

    Salon object is the main object of single salon. It  can contain
    multiple themes, all important dates for salone (start, end, jury
    and results date) and list of judges.

    """
    #: user who created salon
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='salons_owned')

    #: date salon was created
    created = models.DateTimeField(auto_now_add=True)

    #: date salon was last modified
    modified = models.DateTimeField(auto_now=True)

    #: title of the salon
    title = models.CharField(max_length=100)

    #: date when salon starts
    start_date = models.DateField()

    #: date when salon ends
    end_date = models.DateField()

    #: date when judging will take place
    jury_date = models.DateField()

    #: date when results will be published
    results_date = models.DateField()

    #: list of judges
    judges = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='salons_judged')

    def __str__(self):
        """Return salon's title."""
        return self.title

    def is_active(self):
        """Check if salon is active."""
        return self.start_date <= date.today() <= self.end_date
    is_active.admin_order_field = 'end_date'
    is_active.boolean = True


class Theme(models.Model):
    """Model for storing themes.

    Theme object

    """

    #: date theme was created
    created = models.DateTimeField(auto_now_add=True)

    #: date theme was last modified
    modified = models.DateTimeField(auto_now=True)

    #: title of the theme
    title = models.CharField(max_length=100)

    #: salon that theme belongs to
    salon = models.ForeignKey(Salon, related_name='themes')

    #: number of photos that can be submited to theme
    n_photos = models.IntegerField('Number of photos')

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


def generate_file_filename(*args):
    return _generate_filename(*args, 'photos')


def generate_thumb_filename(*args):
    return _generate_filename(*args, 'thumbs')


class File(models.Model):
    """Model for storing uploaded images.

    Uploaded images can be stored prior to creating Photo instance. This
    way you can upload images while user is typing other data.
    Images are checked if meet size and format requirements before
    saving.

    """

    #: date file was created
    created = models.DateTimeField(auto_now_add=True)

    #: date file was last modified
    modified = models.DateTimeField(auto_now=True)

    #: uploaded file
    file = models.ImageField(upload_to=generate_file_filename)

    #: thumbnail of uploaded file
    thumbnail = models.ImageField(upload_to=generate_thumb_filename)

    #: user, who uploaded file
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def save(self, *args, **kwargs):
        """Add photo thumbnail and save object."""
        if not self.pk:  # on create
            image = Image.open(self.file)
            image.thumbnail((100, 100), Image.ANTIALIAS)

            thumb = io.BytesIO()
            image.save(thumb, format="jpeg", quality=100, optimize=True, progressive=True)
            self.thumbnail = InMemoryUploadedFile(thumb, None, self.file.name, 'image/jpeg',
                                                  thumb.tell(), None)

        super(File, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Delete attached images and actual object."""
        self.file.delete(save=False)  # pylint: disable=no-member
        self.thumbnail.delete(save=False)  # pylint: disable=no-member

        super(File, self).delete(*args, **kwargs)

    def get_long_edge(self):
        """Return longer edge of the image."""
        return max(self.file.width, self.file.height)  # pylint: disable=no-member

    def __str__(self):
        photo = self.photo_set.first()  # pylint: disable=no-member
        photo_title = photo.title if photo else '?'
        photo_id = title = photo.pk if photo else '?'
        return "id: {}, filename: {}, photo id: {}, photo title: {}".format(
            self.pk, self.file.name, photo_id, photo_title)


class Author(models.Model):
    """ Model for storing participents.


    """

    #: date ``Author`` was created
    created = models.DateTimeField(auto_now_add=True)

    #: date ``Author`` was last modified
    modified = models.DateTimeField(auto_now=True)

    #: user, wko uploaded ``Author``'s photos
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL)

    #: ``Author``'s first name
    first_name = models.CharField(max_length=30)

    #: ``Author``'s last name
    last_name = models.CharField(max_length=30)

    #: mentor
    mentor = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class Photo(models.Model):
    """Model for storing uploaded photos.



    """
    #: date photo was created
    created = models.DateTimeField(auto_now_add=True)

    #: date photo was last modified
    modified = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=100)

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    author = models.ForeignKey('Author')

    theme = models.ForeignKey(Theme)

    photo = models.ForeignKey(File)

    def __str__(self):
        return self.title
