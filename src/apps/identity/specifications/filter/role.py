from apps.identity.models import Role
from specifications.filter import FilteringSpecificationBase


class RoleFilterSpecification(FilteringSpecificationBase):
    def __init__(self, show_archived: bool = False):
        filters = []

        if not show_archived:
            filters.append(self._Filter(Role.archived_at, "eq", None))

        super().__init__(filters)
