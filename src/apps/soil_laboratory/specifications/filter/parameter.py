from apps.soil_laboratory.models import Parameter
from specifications.filter import FilteringSpecificationBase


class ParameterFilterSpecification(FilteringSpecificationBase):
    def __init__(self, show_archived: bool = False):
        filters = []

        if not show_archived:
            filters.append(self._Filter(Parameter.archived_at, "eq", None))

        super().__init__(filters)
