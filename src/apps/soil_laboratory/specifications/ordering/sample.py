from apps.soil_laboratory.models import Material, MaterialSource, MaterialType, Sample
from specifications.ordering import OrderingField, OrderingSpecificationBase


class SampleOrderingSpecification(OrderingSpecificationBase):
    __ordering_fields__ = (
        OrderingField("materialTypeName", MaterialType.name),
        OrderingField("materialName", Material.name),
        OrderingField("materialSourceName", MaterialSource.name),
        OrderingField("receivedAt", Sample.received_at),
        OrderingField("temperature", Sample.temperature),
        OrderingField("createdAt", Sample.created_at),
        OrderingField("updatedAt", Sample.updated_at),
    )
    __join_paths__ = (Material, MaterialType, MaterialSource,)
    __default_query_param__ = "-receivedAt"

    def __init__(self, query_param: str | None):
        super().__init__(query_param)
