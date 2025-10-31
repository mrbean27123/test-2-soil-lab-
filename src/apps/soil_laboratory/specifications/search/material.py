from apps.soil_laboratory.models import Material, MaterialType
from specifications.search import SearchSpecificationBase


class MaterialSearchSpecification(SearchSpecificationBase):
    def __init__(self, query: str | None = None):
        search_fields = []

        query = self._normalize_search_query(query)

        search_fields.append(self._SearchField(MaterialType.name, "icontains"))
        search_fields.append(self._SearchField(Material.name, "icontains"))

        super().__init__(query, search_fields, join_paths=[MaterialType])
