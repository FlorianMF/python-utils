from enum import Enum, EnumMeta, IntEnum, StrEnum
from typing import Any, Union

from py_utils.types import Str_or_Enum

__all__ = [
    "MyEnum",
    "MyStrEnum",
    "MyIntEnum",
]


class MyEnumMeta(EnumMeta):
    """This adds the ability to do enum.values."""

    @property
    def values(cls) -> list[Any]:
        return [v.value for v in cls.__members__.values()]

    def __contains__(cls, other: Any):
        other = other.value if isinstance(other, Enum) else other
        return other in [v.value for v in cls.__members__.values()]


class MyStrEnumMeta(MyEnumMeta):
    """This allows to simplify the `contains` check from `is 'foo in list(Enum)` to `is 'foo' in Enum` test."""

    def __contains__(cls, other: Str_or_Enum):
        other = other.value if isinstance(other, StrEnum) else str(other)
        return other.lower() in [v.value.lower() for v in cls.__members__.values()]


class MyEnum(Enum, metaclass=MyEnumMeta):
    def __eq__(self, other: Any) -> bool:
        other = other.value if isinstance(other, Enum) else other
        return self.value == other


class MyStrEnum(StrEnum, metaclass=MyStrEnumMeta):
    """Version of StrEnum which allows case-insensitive comparison to a string.

    Example:
        >>> class MyEnum(MyEnum):
        ...     XYZ = 'xyz'
        >>> MyEnum.from_str('XyZ')
        <MyEnum.XYZ: 'xyz'>
        >>> {MyEnum.XYZ: 1234}
        {<MyEnum.XYZ: 'xyz'>: 1234}
    """

    @classmethod
    def from_str(cls, value: str) -> Union["MyStrEnum", None]:
        statuses = [status for status in dir(cls) if not status.startswith("_")]
        for st in statuses:
            if st.lower() == value.lower():
                return getattr(cls, st)
        return None

    def __eq__(self, other: Str_or_Enum) -> bool:
        other = other.value if isinstance(other, StrEnum) else str(other)
        return self.value.lower() == other.lower()

    def __hash__(self):
        # re-enable hashability, such that it can be used in sets or as a dict key
        # example: set(MyStrEnum)
        return hash(self.value.lower())


class MyIntEnum(IntEnum, MyEnum):
    """Adapted version of IntEnum."""