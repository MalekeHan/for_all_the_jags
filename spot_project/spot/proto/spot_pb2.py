# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: spot.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nspot.proto\"v\n\x0bQueryUpdate\x12\x1b\n\x03pan\x18\x01 \x01(\x0b\x32\x0c.LocationPanH\x00\x12\x1d\n\x04zoom\x18\x02 \x01(\x0b\x32\r.LocationZoomH\x00\x12\x1f\n\tparameter\x18\x03 \x01(\x0b\x32\n.ParameterH\x00\x42\n\n\x08location\"\'\n\x0bLocationPan\x12\x0b\n\x03lat\x18\x01 \x01(\x01\x12\x0b\n\x03lon\x18\x02 \x01(\x01\"\x1e\n\x0cLocationZoom\x12\x0e\n\x06radius\x18\x01 \x01(\x01\"B\n\tParameter\x12\x19\n\x04type\x18\x01 \x01(\x0e\x32\x0b.FilterType\x12\r\n\x05value\x18\x02 \x01(\t\x12\x0b\n\x03\x61\x64\x64\x18\x03 \x01(\x08\"d\n\x08Location\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0b\n\x03lat\x18\x02 \x01(\x01\x12\x0b\n\x03lon\x18\x03 \x01(\x01\x12\x0c\n\x04name\x18\x04 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x05 \x01(\t\x12\x12\n\nattributes\x18\x06 \x01(\t**\n\nFilterType\x12\x0c\n\x08\x43\x41TEGORY\x10\x00\x12\x0e\n\nATTRIBUTES\x10\x01\x32\x43\n\x0fLocationService\x12\x30\n\x0fLocationSession\x12\x0c.QueryUpdate\x1a\t.Location\"\x00(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'spot_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_FILTERTYPE']._serialized_start=377
  _globals['_FILTERTYPE']._serialized_end=419
  _globals['_QUERYUPDATE']._serialized_start=14
  _globals['_QUERYUPDATE']._serialized_end=132
  _globals['_LOCATIONPAN']._serialized_start=134
  _globals['_LOCATIONPAN']._serialized_end=173
  _globals['_LOCATIONZOOM']._serialized_start=175
  _globals['_LOCATIONZOOM']._serialized_end=205
  _globals['_PARAMETER']._serialized_start=207
  _globals['_PARAMETER']._serialized_end=273
  _globals['_LOCATION']._serialized_start=275
  _globals['_LOCATION']._serialized_end=375
  _globals['_LOCATIONSERVICE']._serialized_start=421
  _globals['_LOCATIONSERVICE']._serialized_end=488
# @@protoc_insertion_point(module_scope)
