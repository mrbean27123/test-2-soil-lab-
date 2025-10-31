from apps.soil_laboratory.models import Material, MaterialType
from specifications.filter import FilteringSpecificationBase


class MaterialFilterSpecification(FilteringSpecificationBase):
    def __init__(self, material_type_code__eq: str | None = None, show_archived: bool = False):
        filters = []

        if not show_archived:
            filters.append(self._Filter(Material.archived_at, "eq", None))

        parsed_material_type_code__eq = self._parse_material_type_code__eq(material_type_code__eq)
        if parsed_material_type_code__eq:
            filters.append(self._Filter(MaterialType.code, "eq", parsed_material_type_code__eq))

        super().__init__(filters, join_paths=[MaterialType])

    def _parse_material_type_code__eq(
        self,
        material_type_code__eq_str: str
    ) -> str | list[str] | None:
        params = self._extract_list_from_query_param(material_type_code__eq_str)

        if not params:
            return None

        return params[0] if len(params) == 1 else params
