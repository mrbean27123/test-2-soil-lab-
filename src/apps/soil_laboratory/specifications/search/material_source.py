from apps.soil_laboratory.models import MaterialSource
from specifications.search import SearchField, SearchSpecificationBase


class MaterialSourceSearchSpecification(SearchSpecificationBase):
    __search_fields__ = (SearchField("name", MaterialSource.name, "icontains"),)

    def __init__(self, query: str | None):
        super().__init__(query)
