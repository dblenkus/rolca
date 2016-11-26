""".. Ignore pydocstyle D400.

==========
Core Admin
==========

.. autoclass:: rolca.core.admin.ThemeInline
    :members:

.. autoclass:: rolca.core.admin.JudgeInline
    :members:

.. autoclass:: rolca.core.admin.SalonAdmin
    :members:

"""
from django.contrib import admin

from .models import Salon, Theme, File, Photo


class ThemeInline(admin.TabularInline):
    """Inline Theme tabular used in `SalonAdmin`."""

    model = Theme
    extra = 1


class JudgeInline(admin.TabularInline):
    """Inline Judge tabular used in `SalonAdmin`."""

    model = Salon.judges.through  # pylint: disable=no-member


class SalonAdmin(admin.ModelAdmin):
    """Salon configuration."""

    fieldsets = [
        (None, {'fields': ('title',)}),
        ('Dates', {'fields': (('start_date', 'end_date'),
                              ('jury_date', 'results_date'))}),
    ]

    inlines = [ThemeInline, JudgeInline]

    list_display = ('title', 'start_date', 'end_date', 'is_active')
    list_filter = ['start_date', 'end_date', 'results_date']
    search_fields = ['title']


# admin.site.unregister(Groups)

admin.site.register(Salon, SalonAdmin)
admin.site.register(Photo)
admin.site.register(File)
