""".. Ignore pydocstyle D400."""
from rolca.rating.api.views import ContestViewSet, RatingViewSet, SubmissionViewSet

routeList = (
    (r'rating', RatingViewSet),
    (r'judge/contest', ContestViewSet),
    (r'judge/submission', SubmissionViewSet),
)
