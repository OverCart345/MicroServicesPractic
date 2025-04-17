# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: report_service/proto/report.proto
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
    'report_service/proto/report.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!report_service/proto/report.proto\x12\x06report\"@\n\rReportRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0f\n\x07\x66rom_ts\x18\x02 \x01(\x03\x12\r\n\x05to_ts\x18\x03 \x01(\x03\"\xc0\x01\n\x0eReportResponse\x12\x11\n\treport_id\x18\x01 \x01(\t\x12\x14\n\x0ctotal_income\x18\x02 \x01(\x03\x12\x15\n\rtotal_expense\x18\x03 \x01(\x03\x12;\n\x0b\x62y_category\x18\x04 \x03(\x0b\x32&.report.ReportResponse.ByCategoryEntry\x1a\x31\n\x0f\x42yCategoryEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x01:\x02\x38\x01\"%\n\x10GetReportRequest\x12\x11\n\treport_id\x18\x01 \x01(\t\"\xf0\x01\n\nReportData\x12\x11\n\treport_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x14\n\x0cgenerated_at\x18\x03 \x01(\x03\x12\x14\n\x0ctotal_income\x18\x04 \x01(\x01\x12\x15\n\rtotal_expense\x18\x05 \x01(\x01\x12\x37\n\x0b\x62y_category\x18\x06 \x03(\x0b\x32\".report.ReportData.ByCategoryEntry\x12\x0f\n\x07payload\x18\x07 \x01(\x0c\x1a\x31\n\x0f\x42yCategoryEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x01:\x02\x38\x01\x32\x8b\x01\n\rReportService\x12?\n\x0eGenerateReport\x12\x15.report.ReportRequest\x1a\x16.report.ReportResponse\x12\x39\n\tGetReport\x12\x18.report.GetReportRequest\x1a\x12.report.ReportDatab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'report_service.proto.report_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_REPORTRESPONSE_BYCATEGORYENTRY']._loaded_options = None
  _globals['_REPORTRESPONSE_BYCATEGORYENTRY']._serialized_options = b'8\001'
  _globals['_REPORTDATA_BYCATEGORYENTRY']._loaded_options = None
  _globals['_REPORTDATA_BYCATEGORYENTRY']._serialized_options = b'8\001'
  _globals['_REPORTREQUEST']._serialized_start=45
  _globals['_REPORTREQUEST']._serialized_end=109
  _globals['_REPORTRESPONSE']._serialized_start=112
  _globals['_REPORTRESPONSE']._serialized_end=304
  _globals['_REPORTRESPONSE_BYCATEGORYENTRY']._serialized_start=255
  _globals['_REPORTRESPONSE_BYCATEGORYENTRY']._serialized_end=304
  _globals['_GETREPORTREQUEST']._serialized_start=306
  _globals['_GETREPORTREQUEST']._serialized_end=343
  _globals['_REPORTDATA']._serialized_start=346
  _globals['_REPORTDATA']._serialized_end=586
  _globals['_REPORTDATA_BYCATEGORYENTRY']._serialized_start=255
  _globals['_REPORTDATA_BYCATEGORYENTRY']._serialized_end=304
  _globals['_REPORTSERVICE']._serialized_start=589
  _globals['_REPORTSERVICE']._serialized_end=728
# @@protoc_insertion_point(module_scope)
