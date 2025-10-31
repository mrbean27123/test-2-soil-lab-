from apps.soil_laboratory.models import Material, MaterialSource
from specifications.search import SearchSpecificationBase


class SampleSearchSpecification(SearchSpecificationBase):
    def __init__(self, query: str | None = None):
        search_fields = []

        query = self._normalize_search_query(query)

        search_fields.append(self._SearchField(MaterialSource.name, "icontains"))
        search_fields.append(self._SearchField(Material.name, "icontains"))

        super().__init__(query, search_fields, join_paths=[Material, MaterialSource])
