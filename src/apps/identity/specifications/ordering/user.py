from apps.identity.models import User
from specifications.ordering import OrderingField, OrderingSpecificationBase


class UserOrderingSpecification(OrderingSpecificationBase):
    __ordering_fields__ = (
        OrderingField("firstName", User.first_name),
        OrderingField("lastName", User.last_name),
        OrderingField("email", User.email),
        OrderingField("lastLoginAt", User.last_login_at),
        OrderingField("createdAt", User.created_at),
        OrderingField("updatedAt", User.updated_at),
    )
    __default_query_param__ = "-createdAt"

    def __init__(self, query_param: str | None):
        super().__init__(query_param)
