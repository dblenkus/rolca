# pylint: disable=missing-docstring
import unittest

from mock import MagicMock, Mock

from django.contrib.auth import get_user_model

from rolca.core.models import Author
from rolca.frontend.views import UploadView


class UploadViewTest(unittest.TestCase):
    def setUp(self):
        self.view_mock = MagicMock(spec=UploadView)
        self.view_mock.request = Mock()

    def test_create_author(self):
        """Author object with data from request's user is created."""
        user_model = get_user_model()
        user = user_model.objects.create_user(username='u', first_name='Janez', last_name='Novak')
        self.view_mock.request.user = user

        UploadView.create_author(self.view_mock)

        self.assertEqual(Author.objects.count(), 1)

        author = Author.objects.first()
        self.assertEqual(author.first_name, 'Janez')
        self.assertEqual(author.last_name, 'Novak')
        self.assertEqual(author.user, user)

    def test_one_author(self):
        """Only one Author is created for all forms."""
        formset_mock = [
            MagicMock(cleaned_data={'title': 'My image', 'photo': '<my_photo>'}),
            MagicMock(cleaned_data={'title': 'My second image', 'photo': '<my_photo_2>'}),
        ]

        UploadView.form_valid(self.view_mock, formset_mock)

        self.assertEqual(self.view_mock.create_author.call_count, 1)

    def test_empty_form(self):
        """Save is not called for forms with no data."""
        formset_mock = [
            MagicMock(cleaned_data={'title': 'My image', 'photo': '<my_photo>'}),
            MagicMock(cleaned_data={}),
        ]

        UploadView.form_valid(self.view_mock, formset_mock)

        self.assertEqual(formset_mock[0].save.call_count, 1)
        self.assertEqual(formset_mock[1].save.call_count, 0)

    def test_empty_formset(self):
        """No Author object is created if all forms are empty."""
        formset_mock = [
            MagicMock(cleaned_data={}),
            MagicMock(cleaned_data={}),
        ]

        UploadView.form_valid(self.view_mock, formset_mock)

        self.assertEqual(self.view_mock.create_author.call_count, 0)
