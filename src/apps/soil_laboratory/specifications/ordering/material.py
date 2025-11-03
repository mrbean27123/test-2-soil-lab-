from apps.soil_laboratory.models import Material, MaterialType
from specifications.ordering import OrderingField, OrderingSpecificationBase


class MaterialOrderingSpecification(OrderingSpecificationBase):
    __ordering_fields__ = (
        OrderingField("materialTypeName", MaterialType.name),
        OrderingField("name", Material.name),
        OrderingField("createdAt", Material.created_at),
        OrderingField("updatedAt", Material.updated_at),
    )
    __join_paths__ = (MaterialType,)
    __default_query_param__ = "name"

    def __init__(self, query_param: str | None):
        super().__init__(query_param)
