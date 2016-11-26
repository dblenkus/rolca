""".. Ignore pydocstyle D400.

==============
Frontend views
==============

.. autoclass:: rolca.frontend.views.UploadView
    :members:

"""
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from rolca.core.models import Theme, Author
from .forms import ThemeFormSet


class UploadView(FormView):
    """View for uploading photos."""

    template_name = 'frontend/upload.html'
    form_class = ThemeFormSet
    success_url = reverse_lazy('upload_confirm')

    def create_author(self):
        """Create Author object for uploaded photos."""
        return Author.objects.create(
            uploader=self.request.user,
            first_name=self.request.user.first_name,
            last_name=self.request.user.last_name,
        )

    def get_theme(self):
        """Get Theme object for uploaded photos."""
        # XXX: This must be determined in proper way
        return Theme.objects.last()

    def form_valid(self, form_set):
        """Create Author object and call save on all non-empty forms."""
        author = None
        for form in form_set:
            # validation is skipped for empty forms in formset, so we
            # have to check that there are actual data to save
            if form.cleaned_data:
                if not author:
                    author = self.create_author()

                theme = self.get_theme()

                form.save(self.request.user, author, theme)

        return super(UploadView, self).form_valid(form_set)


upload_view = login_required(UploadView.as_view())  # pylint: disable=invalid-name
confirm_view = TemplateView.as_view(  # pylint: disable=invalid-name
    template_name='frontend/upload_confirm.html')


# def list_select(request):
#     salons = Salon.objects.all()

#     response = {'salons': salons}
#     return render(request, os.path.join('frontend', 'list_select.html'),
#                   response)


# def list_details(request, salon_id):
#     salon = get_object_or_404(Salon, pk=salon_id)
#     themes = Theme.objects.filter(salon=salon)

#     response = {'users': []}
#     for user in Profile.objects.all():  # pylint: disable=no-member
#         count = Photo.objects.filter(theme__in=themes, user=user).count()
#         if count > 0:
#             response['users'].append({
#                 'name': user.get_short_name,
#                 'school': user.school,
#                 'count': count})

#     response['salon'] = salon
#     return render(request, os.path.join('frontend', 'list_details.html'),
#                   response)
