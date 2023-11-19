from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FilterType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CATEGORY: _ClassVar[FilterType]
    ATTRIBUTES: _ClassVar[FilterType]
CATEGORY: FilterType
ATTRIBUTES: FilterType

class QueryUpdate(_message.Message):
    __slots__ = ["pan", "zoom", "parameter"]
    PAN_FIELD_NUMBER: _ClassVar[int]
    ZOOM_FIELD_NUMBER: _ClassVar[int]
    PARAMETER_FIELD_NUMBER: _ClassVar[int]
    pan: LocationPan
    zoom: LocationZoom
    parameter: Parameter
    def __init__(self, pan: _Optional[_Union[LocationPan, _Mapping]] = ..., zoom: _Optional[_Union[LocationZoom, _Mapping]] = ..., parameter: _Optional[_Union[Parameter, _Mapping]] = ...) -> None: ...

class LocationPan(_message.Message):
    __slots__ = ["lat", "lon"]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    lat: float
    lon: float
    def __init__(self, lat: _Optional[float] = ..., lon: _Optional[float] = ...) -> None: ...

class LocationZoom(_message.Message):
    __slots__ = ["radius"]
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    radius: float
    def __init__(self, radius: _Optional[float] = ...) -> None: ...

class Parameter(_message.Message):
    __slots__ = ["type", "value", "add"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ADD_FIELD_NUMBER: _ClassVar[int]
    type: FilterType
    value: str
    add: bool
    def __init__(self, type: _Optional[_Union[FilterType, str]] = ..., value: _Optional[str] = ..., add: bool = ...) -> None: ...

class StreamUpdate(_message.Message):
    __slots__ = ["location", "flush"]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    FLUSH_FIELD_NUMBER: _ClassVar[int]
    location: Location
    flush: Flush
    def __init__(self, location: _Optional[_Union[Location, _Mapping]] = ..., flush: _Optional[_Union[Flush, _Mapping]] = ...) -> None: ...

class Location(_message.Message):
    __slots__ = ["id", "lat", "lon", "name", "category", "attributes"]
    ID_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    id: str
    lat: float
    lon: float
    name: str
    category: str
    attributes: str
    def __init__(self, id: _Optional[str] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., name: _Optional[str] = ..., category: _Optional[str] = ..., attributes: _Optional[str] = ...) -> None: ...

class Flush(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
