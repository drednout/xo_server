import yaml
import json
from datetime import datetime


def getSerialiazationAdapter(self, type_id='json'):
    objects = {
        'yaml': SerializationAdapterYaml,
        'json': SerializationAdapterJson,
    }
    return objects.get(type_id, 'json')()


class SerializationAdapter:
    def pack(self, arg_dict):
        raise NotImplementedError
    
    def unpack(self,packet):
        raise NotImplementedError
    

class SerializationAdapterYaml(SerializationAdapter):
    def pack(self, arg_dict):
        return yaml.dump(arg_dict)

    def unpack(self, packet):
        return yaml.load(packet)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)

class SerializationAdapterJson(SerializationAdapter):
    def pack(self, arg_dict):
        return json.dumps(arg_dict, cls=DateTimeEncoder)
    
    def unpack(self, packet):
        return json.loads(packet)
