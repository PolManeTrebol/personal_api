from enum import Enum


# TODO: This enum needs to be modified with the appropriate permissions
class RolesEnum(Enum):
    READ_ONLY = '/consulting/read_only'
    WRITE_ONLY = '/consulting/write_only'
