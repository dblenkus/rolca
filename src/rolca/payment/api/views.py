""".. Ignore pydocstyle D400."""
from rest_framework import viewsets

from rolca.core.api.permissions import IsSuperUser
from rolca.payment.api.filters import PaymentFilter
from rolca.payment.api.serializers import PaymentSerializer
from rolca.payment.models import Payment


class PaymentViewSet(viewsets.ModelViewSet):
    """API viewset for Payment objects."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsSuperUser,)
    filter_class = PaymentFilter
