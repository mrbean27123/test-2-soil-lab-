from apps.identity.models import Permission
from specifications.filter import FilteringSpecificationBase


class PermissionFilterSpecification(FilteringSpecificationBase):
    def __init__(self, show_archived: bool = False):
        filters = []

        if not show_archived:
            filters.append(self._Filter(Permission.archived_at, "eq", None))

        super().__init__(filters)
