from apps.identity.models import User
from specifications.search import SearchField, SearchSpecificationBase


class UserSearchSpecification(SearchSpecificationBase):
    __search_fields__ = (
        SearchField("firstName", User.first_name, "icontains"),
        SearchField("lastName", User.last_name, "icontains"),
        SearchField("email", User.email, "icontains")
    )

    def __init__(self, query: str | None):
        super().__init__(query)
