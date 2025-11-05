from apps.identity.models import Permission
from specifications.ordering import OrderingField, OrderingSpecificationBase


class PermissionOrderingSpecification(OrderingSpecificationBase):
    __ordering_fields__ = (
        OrderingField("name", Permission.name),
        OrderingField("createdAt", Permission.created_at),
        OrderingField("updatedAt", Permission.updated_at),
    )
    __default_query_param__ = "name"

    def __init__(self, query_param: str | None):
        super().__init__(query_param)
