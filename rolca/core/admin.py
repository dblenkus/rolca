""".. Ignore pydocstyle D400.

==========
Core Admin
==========

.. autoclass:: rolca.core.admin.ThemeInline
    :members:

.. autoclass:: rolca.core.admin.ContestAdmin
    :members:

"""
from django.contrib import admin

from .models import Contest, Theme, File, Photo


class ThemeInline(admin.TabularInline):
    """Inline Theme tabular used in `ContestAdmin`."""

    model = Theme
    fields = ('title', 'n_photos')
    extra = 1


class ContestAdmin(admin.ModelAdmin):
    """Contest configuration."""

    fieldsets = [
        (None, {'fields': ('title', 'description')}),
        ('Dates', {'fields': ('start_date', 'end_date', 'publish_date')}),
    ]

    inlines = [ThemeInline]

    list_display = ('title', 'start_date', 'end_date', 'is_active')
    list_filter = ['start_date', 'end_date', 'publish_date']
    search_fields = ['title']

    def save_model(self, request, obj, form, change):
        """Add current user to the model and save it."""
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()


admin.site.register(Contest, ContestAdmin)
admin.site.register(Photo)
admin.site.register(File)
