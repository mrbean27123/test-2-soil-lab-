from apps.soil_laboratory.models import Material, MaterialType
from specifications.search import SearchField, SearchSpecificationBaseN


class MaterialSearchSpecification(SearchSpecificationBaseN):
    __search_fields__ = (
        SearchField("materialTypeName", MaterialType.name, "icontains"),
        SearchField("materialName", Material.name, "icontains"),
    )
    __join_paths__ = (MaterialType,)

    def __init__(self, query: str | None):
        super().__init__(query)
