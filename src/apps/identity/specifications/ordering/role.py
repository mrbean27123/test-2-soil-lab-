from apps.identity.models import Role
from specifications.ordering import OrderingField, OrderingSpecificationBase


class RoleOrderingSpecification(OrderingSpecificationBase):
    __ordering_fields__ = (
        OrderingField("name", Role.name),
        OrderingField("createdAt", Role.created_at),
        OrderingField("updatedAt", Role.updated_at),
    )
    __default_query_param__ = "name"

    def __init__(self, query_param: str | None):
        super().__init__(query_param)
