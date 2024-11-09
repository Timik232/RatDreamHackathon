# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cardio.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='cardio.proto',
  package='cardio',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0c\x63\x61rdio.proto\x12\x06\x63\x61rdio\"\"\n\rCardioRequest\x12\x11\n\tclient_id\x18\x01 \x01(\t\"R\n\nCardioData\x12\x11\n\ttimestamp\x18\x01 \x01(\x05\x12\x0f\n\x07vector1\x18\x02 \x03(\x02\x12\x0f\n\x07vector2\x18\x03 \x03(\x02\x12\x0f\n\x07vector3\x18\x04 \x03(\x02\"7\n\x1aSetWorkingDirectoryRequest\x12\x19\n\x11working_directory\x18\x01 \x01(\t\".\n\x1bSetWorkingDirectoryResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"2\n\x17SetFileToProcessRequest\x12\x17\n\x0f\x66ile_to_process\x18\x01 \x01(\t\"+\n\x18SetFileToProcessResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32\x87\x02\n\rCardioService\x12?\n\x10StreamCardioData\x12\x15.cardio.CardioRequest\x1a\x12.cardio.CardioData0\x01\x12^\n\x13SetWorkingDirectory\x12\".cardio.SetWorkingDirectoryRequest\x1a#.cardio.SetWorkingDirectoryResponse\x12U\n\x10SetFileToProcess\x12\x1f.cardio.SetFileToProcessRequest\x1a .cardio.SetFileToProcessResponseb\x06proto3'
)




_CARDIOREQUEST = _descriptor.Descriptor(
  name='CardioRequest',
  full_name='cardio.CardioRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='client_id', full_name='cardio.CardioRequest.client_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=58,
)


_CARDIODATA = _descriptor.Descriptor(
  name='CardioData',
  full_name='cardio.CardioData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='cardio.CardioData.timestamp', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vector1', full_name='cardio.CardioData.vector1', index=1,
      number=2, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vector2', full_name='cardio.CardioData.vector2', index=2,
      number=3, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vector3', full_name='cardio.CardioData.vector3', index=3,
      number=4, type=2, cpp_type=6, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=60,
  serialized_end=142,
)


_SETWORKINGDIRECTORYREQUEST = _descriptor.Descriptor(
  name='SetWorkingDirectoryRequest',
  full_name='cardio.SetWorkingDirectoryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='working_directory', full_name='cardio.SetWorkingDirectoryRequest.working_directory', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=144,
  serialized_end=199,
)


_SETWORKINGDIRECTORYRESPONSE = _descriptor.Descriptor(
  name='SetWorkingDirectoryResponse',
  full_name='cardio.SetWorkingDirectoryResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='cardio.SetWorkingDirectoryResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=201,
  serialized_end=247,
)


_SETFILETOPROCESSREQUEST = _descriptor.Descriptor(
  name='SetFileToProcessRequest',
  full_name='cardio.SetFileToProcessRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_to_process', full_name='cardio.SetFileToProcessRequest.file_to_process', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=249,
  serialized_end=299,
)


_SETFILETOPROCESSRESPONSE = _descriptor.Descriptor(
  name='SetFileToProcessResponse',
  full_name='cardio.SetFileToProcessResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='cardio.SetFileToProcessResponse.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=301,
  serialized_end=344,
)

DESCRIPTOR.message_types_by_name['CardioRequest'] = _CARDIOREQUEST
DESCRIPTOR.message_types_by_name['CardioData'] = _CARDIODATA
DESCRIPTOR.message_types_by_name['SetWorkingDirectoryRequest'] = _SETWORKINGDIRECTORYREQUEST
DESCRIPTOR.message_types_by_name['SetWorkingDirectoryResponse'] = _SETWORKINGDIRECTORYRESPONSE
DESCRIPTOR.message_types_by_name['SetFileToProcessRequest'] = _SETFILETOPROCESSREQUEST
DESCRIPTOR.message_types_by_name['SetFileToProcessResponse'] = _SETFILETOPROCESSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CardioRequest = _reflection.GeneratedProtocolMessageType('CardioRequest', (_message.Message,), {
  'DESCRIPTOR' : _CARDIOREQUEST,
  '__module__' : 'cardio_pb2'
  # @@protoc_insertion_point(class_scope:cardio.CardioRequest)
  })
_sym_db.RegisterMessage(CardioRequest)

CardioData = _reflection.GeneratedProtocolMessageType('CardioData', (_message.Message,), {
  'DESCRIPTOR' : _CARDIODATA,
  '__module__' : 'cardio_pb2'
  # @@protoc_insertion_point(class_scope:cardio.CardioData)
  })
_sym_db.RegisterMessage(CardioData)

SetWorkingDirectoryRequest = _reflection.GeneratedProtocolMessageType('SetWorkingDirectoryRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETWORKINGDIRECTORYREQUEST,
  '__module__' : 'cardio_pb2'
  # @@protoc_insertion_point(class_scope:cardio.SetWorkingDirectoryRequest)
  })
_sym_db.RegisterMessage(SetWorkingDirectoryRequest)

SetWorkingDirectoryResponse = _reflection.GeneratedProtocolMessageType('SetWorkingDirectoryResponse', (_message.Message,), {
  'DESCRIPTOR' : _SETWORKINGDIRECTORYRESPONSE,
  '__module__' : 'cardio_pb2'
  # @@protoc_insertion_point(class_scope:cardio.SetWorkingDirectoryResponse)
  })
_sym_db.RegisterMessage(SetWorkingDirectoryResponse)

SetFileToProcessRequest = _reflection.GeneratedProtocolMessageType('SetFileToProcessRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETFILETOPROCESSREQUEST,
  '__module__' : 'cardio_pb2'
  # @@protoc_insertion_point(class_scope:cardio.SetFileToProcessRequest)
  })
_sym_db.RegisterMessage(SetFileToProcessRequest)

SetFileToProcessResponse = _reflection.GeneratedProtocolMessageType('SetFileToProcessResponse', (_message.Message,), {
  'DESCRIPTOR' : _SETFILETOPROCESSRESPONSE,
  '__module__' : 'cardio_pb2'
  # @@protoc_insertion_point(class_scope:cardio.SetFileToProcessResponse)
  })
_sym_db.RegisterMessage(SetFileToProcessResponse)



_CARDIOSERVICE = _descriptor.ServiceDescriptor(
  name='CardioService',
  full_name='cardio.CardioService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=347,
  serialized_end=610,
  methods=[
  _descriptor.MethodDescriptor(
    name='StreamCardioData',
    full_name='cardio.CardioService.StreamCardioData',
    index=0,
    containing_service=None,
    input_type=_CARDIOREQUEST,
    output_type=_CARDIODATA,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SetWorkingDirectory',
    full_name='cardio.CardioService.SetWorkingDirectory',
    index=1,
    containing_service=None,
    input_type=_SETWORKINGDIRECTORYREQUEST,
    output_type=_SETWORKINGDIRECTORYRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='SetFileToProcess',
    full_name='cardio.CardioService.SetFileToProcess',
    index=2,
    containing_service=None,
    input_type=_SETFILETOPROCESSREQUEST,
    output_type=_SETFILETOPROCESSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_CARDIOSERVICE)

DESCRIPTOR.services_by_name['CardioService'] = _CARDIOSERVICE

# @@protoc_insertion_point(module_scope)
