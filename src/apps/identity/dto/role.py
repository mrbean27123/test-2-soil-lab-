from dto import CreateDTOBase, UpdateDTOBase


class RoleCreateDTO(CreateDTOBase):
    code: str
    name: str
    description: str | None = None


class RoleUpdateDTO(UpdateDTOBase):
    code: str | None = None
    name: str | None = None
    description: str | None = None
