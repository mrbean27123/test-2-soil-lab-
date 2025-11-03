from apps.soil_laboratory.models import MaterialType
from specifications.search import SearchField, SearchSpecificationBaseN


class MaterialTypeSearchSpecification(SearchSpecificationBaseN):
    __search_fields__ = (SearchField("name", MaterialType.name, "icontains"),)

    def __init__(self, query: str | None):
        super().__init__(query)
