""".. Ignore pydocstyle D400.

===================
Payment API filters
===================

"""
from django_filters import rest_framework as filters

from rolca.payment.models import Payment


class PaymentFilter(filters.FilterSet):
    """Filter for Submission API endpoint."""

    class Meta:
        model = Payment
        fields = {
            "submissionset": ["exact", "in"],
            "paid": ["exact"],
        }

    def __init__(self, *args, **kwargs):
        print(self.get_filters().keys())
        return super().__init__(*args, **kwargs)
