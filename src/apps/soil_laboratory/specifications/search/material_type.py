from apps.soil_laboratory.models import MaterialType
from specifications.search import SearchSpecificationBase


class MaterialTypeSearchSpecification(SearchSpecificationBase):
    def __init__(self, query: str | None = None):
        search_fields = []

        query = self._normalize_search_query(query)

        search_fields.append(self._SearchField(MaterialType.name, "icontains"))

        super().__init__(query, search_fields)
