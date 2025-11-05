from apps.identity.models import Role
from specifications.search import SearchField, SearchSpecificationBase


class RoleSearchSpecification(SearchSpecificationBase):
    __search_fields__ = (SearchField("name", Role.name, "icontains"),)

    def __init__(self, query: str | None):
        super().__init__(query)
