# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: transaction_service/proto/transaction.proto
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
    'transaction_service/proto/transaction.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+transaction_service/proto/transaction.proto\x12\x0btransaction\"\xb0\x01\n\x15\x41\x64\x64TransactionRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0e\n\x06\x61mount\x18\x02 \x01(\x01\x12\x10\n\x08\x63urrency\x18\x03 \x01(\t\x12*\n\x04type\x18\x04 \x01(\x0e\x32\x1c.transaction.TransactionType\x12\x10\n\x08\x63\x61tegory\x18\x05 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x06 \x01(\t\x12\x11\n\ttimestamp\x18\x07 \x01(\x03\"0\n\x16\x41\x64\x64TransactionResponse\x12\x16\n\x0etransaction_id\x18\x01 \x01(\t\">\n\x0bListRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x0f\n\x07\x66rom_ts\x18\x02 \x01(\x03\x12\r\n\x05to_ts\x18\x03 \x01(\x03\"7\n\x0cListResponse\x12\'\n\x05items\x18\x01 \x03(\x0b\x32\x18.transaction.Transaction\"\xbe\x01\n\x0bTransaction\x12\x16\n\x0etransaction_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x0e\n\x06\x61mount\x18\x03 \x01(\x01\x12\x10\n\x08\x63urrency\x18\x04 \x01(\t\x12*\n\x04type\x18\x05 \x01(\x0e\x32\x1c.transaction.TransactionType\x12\x10\n\x08\x63\x61tegory\x18\x06 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x07 \x01(\t\x12\x11\n\ttimestamp\x18\x08 \x01(\x03**\n\x0fTransactionType\x12\n\n\x06INCOME\x10\x00\x12\x0b\n\x07\x45XPENSE\x10\x01\x32\xb8\x01\n\x12TransactionService\x12Y\n\x0e\x41\x64\x64Transaction\x12\".transaction.AddTransactionRequest\x1a#.transaction.AddTransactionResponse\x12G\n\x10ListTransactions\x12\x18.transaction.ListRequest\x1a\x19.transaction.ListResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'transaction_service.proto.transaction_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TRANSACTIONTYPE']._serialized_start=603
  _globals['_TRANSACTIONTYPE']._serialized_end=645
  _globals['_ADDTRANSACTIONREQUEST']._serialized_start=61
  _globals['_ADDTRANSACTIONREQUEST']._serialized_end=237
  _globals['_ADDTRANSACTIONRESPONSE']._serialized_start=239
  _globals['_ADDTRANSACTIONRESPONSE']._serialized_end=287
  _globals['_LISTREQUEST']._serialized_start=289
  _globals['_LISTREQUEST']._serialized_end=351
  _globals['_LISTRESPONSE']._serialized_start=353
  _globals['_LISTRESPONSE']._serialized_end=408
  _globals['_TRANSACTION']._serialized_start=411
  _globals['_TRANSACTION']._serialized_end=601
  _globals['_TRANSACTIONSERVICE']._serialized_start=648
  _globals['_TRANSACTIONSERVICE']._serialized_end=832
# @@protoc_insertion_point(module_scope)
