from apps.soil_laboratory.models import MaterialSource
from specifications.ordering import OrderingField, OrderingSpecificationBase


class MaterialSourceOrderingSpecification(OrderingSpecificationBase):
    __ordering_fields__ = (
        OrderingField("name", MaterialSource.name),
        OrderingField("createdAt", MaterialSource.created_at),
        OrderingField("updatedAt", MaterialSource.updated_at),
    )
    __default_query_param__ = "name"

    def __init__(self, query_param: str | None):
        super().__init__(query_param)
