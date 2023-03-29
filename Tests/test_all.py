from Tests.test_domain import test_all_domain
from Tests.test_repository import test_all_repository
from Tests.test_service import test_all_service


def test_all():
    test_all_domain()
    test_all_repository()
    test_all_service()
