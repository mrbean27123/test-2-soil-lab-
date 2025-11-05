from apps.soil_laboratory.models import Material, MaterialSource
from specifications.search import SearchField, SearchSpecificationBase


class SampleSearchSpecification(SearchSpecificationBase):
    __search_fields__ = (
        SearchField("materialName", Material.name, "icontains"),
        SearchField("materialSourceName", MaterialSource.name, "icontains")
    )
    __join_paths__ = (Material, MaterialSource)

    def __init__(self, query: str | None):
        super().__init__(query)
