from enum import Enum

class FileContentType(Enum):
    MULTICOLUMN = "multiColumn"
    TABLE = "table"
    STANDARD = "standard"
    CONTAINS_TABLE = "containTable"