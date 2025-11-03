from apps.soil_laboratory.models import Parameter
from specifications.search import SearchField, SearchSpecificationBaseN


class ParameterSearchSpecification(SearchSpecificationBaseN):
    __search_fields__ = (
        SearchField("name", Parameter.name, "icontains"),
        SearchField("units", Parameter.units, "icontains"),
    )

    def __init__(self, query: str | None):
        super().__init__(query)
