from dto import CreateDTOBase, UpdateDTOBase


class PermissionCreateDTO(CreateDTOBase):
    code: str
    name: str
    description: str | None = None


class PermissionUpdateDTO(UpdateDTOBase):
    code: str | None = None
    name: str | None = None
    description: str | None = None
