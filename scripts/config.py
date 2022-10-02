import json

class Config(object):
    def __init__(self, config_path:str = "user_data/configs/config.json"):
        self.config_path = config_path

    def _load_config(self, config_path: str):
        print("Loading conf:" + config_path)
        config_file = open(config_path)
        self.config = json.load(config_file)
        config_file.close()

    def __new__(cls, config_path, _cache={}):
        try:
            return _cache[config_path]
        except KeyError:
            # you must call __new__ on the base class
            x = super(Config, cls).__new__(cls)
            x.__init__(config_path)
            x._load_config(config_path)
            _cache[config_path] = x
            return x

    def get(self, attr: str):
        return self.config[attr]

