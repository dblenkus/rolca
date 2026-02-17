from django.urls import reverse

from rolca.urls import route_lists, router


def test_route_prefixes_are_unique():
    prefixes = [prefix for route_list in route_lists for prefix, _ in route_list]
    assert len(prefixes) == len(set(prefixes))


def test_router_basenames_are_unique():
    basenames = [basename for _, _, basename in router.registry]
    assert len(basenames) == len(set(basenames))


def test_api_routes_are_reversible():
    assert reverse('rolca-core-api:contest-list') == '/api/contest/'
    assert reverse('rolca-core-api:judge-contest-list') == '/api/judge/contest/'
    assert reverse('rolca-core-api:results-theme-detail', kwargs={'pk': 42}) == '/api/results/theme/42/'


def test_download_route_is_reversible():
    assert reverse('rolca-core:download-contest', kwargs={'contest_id': 42}) == '/core/contest/42/download'
