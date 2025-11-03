from apps.soil_laboratory.models import Parameter
from specifications.ordering import OrderingField, OrderingSpecificationBase


class ParameterOrderingSpecification(OrderingSpecificationBase):
    __ordering_fields__ = (
        OrderingField("name", Parameter.name),
        OrderingField("units", Parameter.units),
        OrderingField("createdAt", Parameter.created_at),
        OrderingField("updatedAt", Parameter.updated_at),
    )
    __default_query_param__ = "name"

    def __init__(self, query_param: str | None):
        super().__init__(query_param)
