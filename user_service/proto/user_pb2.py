# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: user_service/proto/user.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'user_service/proto/user.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1duser_service/proto/user.proto\x12\x04user\"D\n\x0fRegisterRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\"#\n\x10RegisterResponse\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"/\n\x0cLoginRequest\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x1e\n\rLoginResponse\x12\r\n\x05token\x18\x01 \x01(\t\"$\n\x11GetProfileRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\"\x91\x01\n\x0bUserProfile\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\x14\n\x0c\x64isplay_name\x18\x04 \x01(\t\x12\x12\n\navatar_url\x18\x05 \x01(\t\x12\x12\n\ncreated_at\x18\x06 \x01(\x03\x12\x12\n\nupdated_at\x18\x07 \x01(\x03\x32\xb4\x01\n\x0bUserService\x12\x39\n\x08Register\x12\x15.user.RegisterRequest\x1a\x16.user.RegisterResponse\x12\x30\n\x05Login\x12\x12.user.LoginRequest\x1a\x13.user.LoginResponse\x12\x38\n\nGetProfile\x12\x17.user.GetProfileRequest\x1a\x11.user.UserProfileb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'user_service.proto.user_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REGISTERREQUEST']._serialized_start=39
  _globals['_REGISTERREQUEST']._serialized_end=107
  _globals['_REGISTERRESPONSE']._serialized_start=109
  _globals['_REGISTERRESPONSE']._serialized_end=144
  _globals['_LOGINREQUEST']._serialized_start=146
  _globals['_LOGINREQUEST']._serialized_end=193
  _globals['_LOGINRESPONSE']._serialized_start=195
  _globals['_LOGINRESPONSE']._serialized_end=225
  _globals['_GETPROFILEREQUEST']._serialized_start=227
  _globals['_GETPROFILEREQUEST']._serialized_end=263
  _globals['_USERPROFILE']._serialized_start=266
  _globals['_USERPROFILE']._serialized_end=411
  _globals['_USERSERVICE']._serialized_start=414
  _globals['_USERSERVICE']._serialized_end=594
# @@protoc_insertion_point(module_scope)
