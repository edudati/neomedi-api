import enum

class UserRole(enum.Enum):
    """Enum to user roles"""
    SUPER = "super"
    PROFESSIONAL = "professional"
    CLIENT = "client"

class Gender(enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNDISCLOSED = "undisclosed"