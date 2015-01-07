import yaml


class SerializationAdapterFactory(object):
    def __init__(self, is_client=False):
        self.objects = {
            'yaml': SerializationAdapterYaml,
            'json': SerializationAdapterJson,
        }
    
    def getSeriliazationAdapter(self, type_id='json'):
        return self.objects.get(type_id, 'json')()


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


class SerializationAdapterJson(SerializationAdapter):
    def pack(self, arg_dict):
        import json
        return json.dumps(arg_dict)
    
    def unpack(self, packet):
        import json
        return json.loads(packet)
