from apps.soil_laboratory.models import MaterialType
from specifications.filter import FilteringSpecificationBase


class MaterialTypeFilterSpecification(FilteringSpecificationBase):
    def __init__(self, show_archived: bool = False):
        filters = []

        if not show_archived:
            filters.append(self._Filter(MaterialType.archived_at, "eq", None))

        super().__init__(filters)
