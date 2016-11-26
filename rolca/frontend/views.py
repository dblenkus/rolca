""".. Ignore pydocstyle D400.

==============
Frontend views
==============

.. autoclass:: rolca.frontend.views.UploadView
    :members:

.. autoclass:: rolca.frontend.views.SelectContestView
    :members:

"""
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from rolca.core.models import Author, Contest, Theme
from .forms import ThemeFormSet


class UploadView(FormView):
    """View for uploading photos."""

    contest_id = None

    template_name = 'frontend/upload.html'
    form_class = ThemeFormSet
    success_url = reverse_lazy('rolca-frontend:upload_confirm')

    def dispatch(self, request, *args, **kwargs):
        """Self contest id and dispatch request."""
        self.contest_id = kwargs.pop('contest_id')
        return super(UploadView, self).dispatch(request, *args, **kwargs)

    def create_author(self):
        """Create Author object for uploaded photos."""
        return Author.objects.create(
            user=self.request.user,
            first_name=self.request.user.first_name,
            last_name=self.request.user.last_name,
        )

    def get_theme(self):
        """Get Theme object for uploaded photos."""
        return Theme.objects.filter(contest_id=self.contest_id).first()

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


class SelectContestView(ListView):
    """View for selecting the Salon."""

    now = datetime.now()

    queryset = Contest.objects.filter(start_date__lte=now, end_date__gte=now)
    template_name = 'frontend/select_contest.html'

    def get(self, request, *args, **kwargs):
        """Redirect to upload if only one contest is active."""
        queryset = self.get_queryset()
        if queryset.count() == 1:
            contest_pk = queryset.first().pk
            return redirect('rolca-frontend:upload', contest_id=contest_pk)

        return super(SelectContestView, self).get(request, *args, **kwargs)


select_contest_view = SelectContestView.as_view()  # pylint: disable=invalid-name


# def list_details(request, contest_id):
#     contest = get_object_or_404(Contest, pk=contest_id)
#     themes = Theme.objects.filter(contest=contest)

#     response = {'users': []}
#     for user in Profile.objects.all():  # pylint: disable=no-member
#         count = Photo.objects.filter(theme__in=themes, user=user).count()
#         if count > 0:
#             response['users'].append({
#                 'name': user.get_short_name,
#                 'school': user.school,
#                 'count': count})

#     response['contest'] = contest
#     return render(request, os.path.join('frontend', 'list_details.html'),
#                   response)
