# pylint: disable=missing-docstring
from datetime import date, timedelta
import unittest

from rolca.core.models import Author, Photo, Salon, Theme


class DatabaseTestCase(unittest.TestCase):
    def test_salon_str(self):
        salon = Salon(title="Test salon")
        self.assertEqual(str(salon), "Test salon")

    def test_salon_active(self):
        salon = Salon()
        today = date.today()
        day = timedelta(days=1)

        # active salon
        salon.start_date = today - day
        salon.end_date = today + day
        self.assertTrue(salon.is_active())

        # past salon
        salon.start_date = today - 2 * day
        salon.end_date = today - day
        self.assertFalse(salon.is_active())

        # future salon
        salon.start_date = today + day
        salon.end_date = today + 2 * day
        self.assertFalse(salon.is_active())

    def test_theme_str(self):
        theme = Theme(title="Test theme")
        self.assertEqual(str(theme), "Test theme")

    def test_file_str(self):
        # TODO
        pass

    def test_participant_str(self):
        participent = Author(first_name="Janez", last_name="Novak")
        self.assertEqual(str(participent), "Janez Novak")

    def test_photo_str(self):
        photo = Photo(title="Test photo")
        self.assertEqual(str(photo), "Test photo")
