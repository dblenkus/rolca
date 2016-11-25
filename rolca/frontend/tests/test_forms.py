# pylint: disable=missing-docstring
from datetime import date
from mock import patch

from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.test import override_settings, TestCase

from rolca.core.models import Author, File, Photo, Salon, Theme
from rolca.frontend.forms import PhotoForm
from rolca.frontend.tests.utils import get_image_field


class PhotoFormTest(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(username='user')

    def tearDown(self):
        for file_ in File.objects.all():
            file_.file.delete()
            file_.thumbnail.delete()

    def test_pass(self):
        today = date.today()
        salon = Salon.objects.create(owner=self.user, title='Test salon', start_date=today,
                                     end_date=today, jury_date=today, results_date=today)
        theme = Theme.objects.create(title='Test theme', salon=salon, n_photos=2)
        author = Author.objects.create(uploader=self.user)

        form = PhotoForm(data={'title': 'My image'}, files={'photo': get_image_field()})
        form.is_valid()  # generate cleaned_data attribute

        form.save(user=self.user, author=author, theme=theme)

        self.assertEqual(File.objects.count(), 1)
        self.assertEqual(Photo.objects.count(), 1)

    @patch('rolca.frontend.forms.Photo')
    def test_transaction(self, photo_patch):
        photo_patch.objects.create.side_effect = IntegrityError

        form = PhotoForm(data={'title': 'My image'}, files={'photo': get_image_field()})
        form.is_valid()  # generate cleaned_data attribute

        with self.assertRaises(IntegrityError):
            form.save(user=self.user, author='', theme='')

        self.assertEqual(File.objects.count(), 0)

    @override_settings(ROLCA_MAX_SIZE=1)
    def test_file_size_validation(self):
        form = PhotoForm(data={'title': 'My image'}, files={'photo': get_image_field()})
        self.assertFalse(form.is_valid())

    @override_settings(ROLCA_MAX_LONG_EDGE=50)
    def test_long_edge_validation(self):
        form = PhotoForm(data={'title': 'My image'}, files={'photo': get_image_field()})
        self.assertFalse(form.is_valid())

    @override_settings(ROLCA_ACCEPTED_FORMATS=['png'])
    def test_file_format_validation(self):
        form = PhotoForm(data={'title': 'My image'}, files={'photo': get_image_field()})
        self.assertFalse(form.is_valid())
