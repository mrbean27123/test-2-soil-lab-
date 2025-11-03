from apps.soil_laboratory.models import MaterialType
from specifications.ordering import OrderingField, OrderingSpecificationBase


class MaterialTypeOrderingSpecification(OrderingSpecificationBase):
    __ordering_fields__ = (
        OrderingField("name", MaterialType.name),
        OrderingField("createdAt", MaterialType.created_at),
        OrderingField("updatedAt", MaterialType.updated_at),
    )
    __default_query_param__ = "name"

    def __init__(self, query_param: str | None):
        super().__init__(query_param)
