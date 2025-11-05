from apps.soil_laboratory.models import MaterialSource
from specifications.filter import FilteringSpecificationBase


class MaterialSourceFilterSpecification(FilteringSpecificationBase):
    def __init__(self, show_archived: bool = False):
        filters = []

        if not show_archived:
            filters.append(self._Filter(MaterialSource.archived_at, "eq", None))

        super().__init__(filters)
