import io
import requests
from urllib.parse import urljoin
from avro.schema import Parse
from avro.io import DatumWriter, DatumReader, BinaryEncoder, BinaryDecoder


#
# Get the binary encoding for the provided object, using the
# provided Avro schema definition.
#
# @param myschema - Avro schema object
# @param myobject - Python object to be serialized
#
# @returns bytes representation of the binary-encoded serialized object
def serialize(myschema, myobject):
    buf = io.BytesIO()
    encoder = BinaryEncoder(buf)
    writer = DatumWriter(writer_schema=myschema)
    writer.write(myobject, encoder)
    buf.seek(0)
    return (buf.read())


#
# Extracts a Python object from a binary-encoded serialization
# using the provided Avro schema definition.
#
# @param myschema - Avro schema object
# @param mydata   - bytes to be deserialized
#
# @returns Python object deserialized from the provided bytes
def deserialize(myschema, mydata):
    buf = io.BytesIO(mydata)
    decoder = BinaryDecoder(buf)
    reader = DatumReader(writer_schema=myschema)
    return (reader.read(decoder))


#
# Returns an Avro schema definition from the specified local file.
#
# @param filename - location of an Avro avsc schema definition file
#
# @returns Avro schema object
def get_schema_from_file(filename):
    return Parse(open(filename, "rb").read())


#
# Retrieves an Avro schema object from the Event Streams Schema Registry
#
# @param schemaid      - string - ID for the schema to retrieve
# @param schemaversion - string - Version ID for the schema to retrieve
# @param restapi       - string - URL for the Schema Registry
# @param apikey        - string - API key for accessing the Schema Registry
# @param cert          - string - location of a PEM file for accessing the Schema Registry
#
# @returns Avro schema object
def get_schema_from_registry(schemaid, schemaversion, restapi, apikey, cert):
    url=urljoin(restapi, "/schemas/" + schemaid + "/versions/" + schemaversion)
    headers={ "Accept":"application/vnd.apache.avro+json" }

    r = requests.get(url, auth=("token", apikey), headers=headers, verify=cert)
    if r.status_code == 200:
        return Parse(r.text)
    else:
        raise Exception(r.text)


#
# Helper function for preparing Kafka message headers for sending a message
# using a schema.
#
# @param schemaid      - string - ID for the schema being used
# @param schemaversion - string - Version ID for the schema being used
#
# @returns list of tuples ready for use as headers in a Kafka message
def create_headers_for_schema(schemaid, schemaversion):
    return [
        ( "com.ibm.eventstreams.schemaregistry.schema.id", schemaid.encode() ),
        ( "com.ibm.eventstreams.schemaregistry.schema.version", schemaversion.encode() ),
        ( "com.ibm.eventstreams.schemaregistry.encoding", b"BINARY" )
    ]


#
# Retrieves an Avro schema from the Event Streams Schema Registry for
# the provided Kafka message.
#
# The schema to retrieve is identified by the headers on the Kafka
# message.
#
# @param kafka_message - object - msg object returned by a KafkaConsumer
# @param restapi       - string - URL for the Schema Registry
# @param apikey        - string - API key for accessing the Schema Registry
# @param cert          - string - location of a PEM file for accessing the Schema Registry
#
# @returns Avro schema object, or None if the required headers are not found
def get_schema_from_message(kafka_message, restapi, apikey, cert):
    schemaid = None
    schemaversion = None

    for header in kafka_message.headers:
        if header[0] == "com.ibm.eventstreams.schemaregistry.schema.id":
            schemaid = header[1].decode()
        elif header[0] == "com.ibm.eventstreams.schemaregistry.schema.version":
            schemaversion = header[1].decode()

    if schemaid and schemaversion:
        return get_schema(schemaid, schemaversion, restapi, apikey, cert)
    else:
        return None


# a local cache of Avro schema definitions to avoid
# schemas needing to be downloaded multiple times
schema_cache = {}


#
# Retrieves a schema from the local cache
#
# @param schemaid      - string - ID for the schema to retrieve
# @param schemaversion - string - Version ID for the schema to retrieve
#
# @returns Avro schema definition, or None if not found in the cache
def get_schema_from_cache(schemaid, schemaversion):
    if schemaid in schema_cache:
        if schemaversion in schema_cache[schemaid]:
            return schema_cache[schemaid][schemaversion]
    else:
        schema_cache[schemaid] = {}
    return None


#
# Retrieves the specified schema from the Event Streams Schema Registry.
#
# @param schemaid      - string - ID for the schema to retrieve
# @param schemaversion - string - Version ID for the schema to retrieve
# @param restapi       - string - URL for the Schema Registry
# @param apikey        - string - API key for accessing the Schema Registry
# @param cert          - string - location of a PEM file for accessing the Schema Registry
#
# @returns Avro schema definition
def get_schema(schemaid, schemaversion, restapi, apikey, cert):
    schema = get_schema_from_cache(schemaid, schemaversion)
    if schema is None:
        schema = get_schema_from_registry(schemaid, schemaversion, restapi, apikey, cert)
    schema_cache[schemaid][schemaversion] = schema
    return schema
