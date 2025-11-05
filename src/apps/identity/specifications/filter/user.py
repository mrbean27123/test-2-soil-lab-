from apps.identity.models import User
from specifications.filter import FilteringSpecificationBase


class UserFilterSpecification(FilteringSpecificationBase):
    def __init__(self, show_deleted: bool = False):
        filters = []

        if not show_deleted:
            filters.append(self._Filter(User.deleted_at, "eq", None))

        super().__init__(filters)
