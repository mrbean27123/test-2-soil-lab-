from apps.identity.models import Permission
from specifications.search import SearchField, SearchSpecificationBase


class PermissionSearchSpecification(SearchSpecificationBase):
    __search_fields__ = (SearchField("name", Permission.name, "icontains"),)

    def __init__(self, query: str | None):
        super().__init__(query)
