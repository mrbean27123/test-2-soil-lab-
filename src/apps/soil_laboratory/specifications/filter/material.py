from apps.soil_laboratory.models import MaterialType
from specifications.filter import FilteringSpecificationBase


class MaterialFilterSpecification(FilteringSpecificationBase):
    def __init__(self, material_type_code__eq: str | None = None):
        filters = []

        if material_type_code__eq:
            filters.append(
                self._Filter(
                    MaterialType.code,
                    "eq",
                    material_type_code__eq,
                    join_path=MaterialType
                )
            )

        super().__init__(filters)
