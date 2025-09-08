from pydantic import BaseModel


class CreateDTOBase(BaseModel):
    """
    Base class for all Create data transfer objects.

    All DTO classes used for Create operations should inherit from this class to ensure type safety.
    """
    pass


class UpdateDTOBase(BaseModel):
    """
    Base class for all Update data transfer objects.

    All DTO classes used for Update operations should inherit from this class to ensure type safety.
    """
    pass
