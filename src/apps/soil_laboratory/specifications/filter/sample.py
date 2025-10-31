from apps.soil_laboratory.models import Material, MaterialSource, MaterialType, Sample
from specifications.filter import FilteringSpecificationBase


class SampleFilterSpecification(FilteringSpecificationBase):
    def __init__(
        self,
        material_type_id__eq: str | None = None,
        material_type_code__eq: str | None = None,
        material_id__eq: str | None = None,
        material_source_id__eq: str | None = None,
        material_source_code__eq: str | None = None,
        show_deleted: bool = False
    ):
        filters = []

        if not show_deleted:
            filters.append(self._Filter(Sample.deleted_at, "eq", None))

        parsed_material_type_id__eq = self._parse_material_type_id__eq(material_type_id__eq)
        if parsed_material_type_id__eq:
            filters.append(self._Filter(MaterialType.id, "eq", parsed_material_type_id__eq))

        parsed_material_type_code__eq = self._parse_material_type_code__eq(material_type_code__eq)
        if parsed_material_type_code__eq:
            filters.append(self._Filter(MaterialType.code, "eq", parsed_material_type_code__eq))

        parsed_material_id__eq = self._parse_material_id__eq(material_id__eq)
        if parsed_material_id__eq:
            filters.append(self._Filter(Material.id, "eq", parsed_material_id__eq))

        parsed_material_source_id__eq = self._parse_material_source_id__eq(material_source_id__eq)
        if parsed_material_source_id__eq:
            filters.append(self._Filter(MaterialSource.id, "eq", parsed_material_source_id__eq))

        parsed_material_source_code__eq = (
            self._parse_material_source_code__eq(material_source_code__eq)
        )
        if parsed_material_source_code__eq:
            filters.append(self._Filter(MaterialSource.code, "eq", parsed_material_source_code__eq))

        super().__init__(filters, join_paths=[Material, MaterialType, MaterialSource])

    def _parse_material_type_id__eq(
        self,
        material_type_id__eq_str: str
    ) -> str | list[str] | None:
        return self._parse_string_params(material_type_id__eq_str)

    def _parse_material_type_code__eq(
        self,
        material_type_code__eq_str: str
    ) -> str | list[str] | None:
        return self._parse_string_params(material_type_code__eq_str)

    def _parse_material_id__eq(self, material_id__eq_str: str) -> str | list[str] | None:
        return self._parse_string_params(material_id__eq_str)

    def _parse_material_source_id__eq(
        self,
        material_source_id__eq_str: str
    ) -> str | list[str] | None:
        return self._parse_string_params(material_source_id__eq_str)

    def _parse_material_source_code__eq(
        self,
        material_source_code__eq_str: str
    ) -> str | list[str] | None:
        return self._parse_string_params(material_source_code__eq_str)

    def _parse_string_params(self, value: str) -> str | list[str] | None:
        if not (str_params := self._extract_list_from_query_param(value)):
            return None

        return str_params if len(str_params) > 1 else str_params[0]
