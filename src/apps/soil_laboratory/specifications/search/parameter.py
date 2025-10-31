from apps.soil_laboratory.models import Parameter
from specifications.search import SearchSpecificationBase


class ParameterSearchSpecification(SearchSpecificationBase):
    def __init__(self, query: str | None = None):
        search_fields = []

        query = self._normalize_search_query(query)

        search_fields.append(self._SearchField(Parameter.name, "icontains"))
        search_fields.append(self._SearchField(Parameter.units, "icontains"))

        super().__init__(query, search_fields)
