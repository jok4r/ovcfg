import os
import json
import pathlib


config_paths = {
    "posix": [
        '/etc',
        os.path.join(os.path.expanduser("~"), '.config')
    ],
    'nt': [
        os.getenv('APPDATA')
    ]
}


class Config(object):
    def __init__(
            self,
            std_config=None,
            file='example.cfg',
            cfg_dir_name='example_config_dir',
            local=False,
            dir_path=None,
            sort_keys=False
    ):
        self.config_paths = config_paths
        if std_config is None:
            std_config = {}
        self.std_config = std_config
        self.file = file
        self.cfg_dir_name = cfg_dir_name
        if local and dir_path:
            raise ValueError('If local is True, dir_path cannot be defined!')
        if local:
            config_path = pathlib.Path().absolute()
            self.dir_path = config_path
        else:
            self.dir_path = None
        self.sort_keys = sort_keys

    def get_full_path(self, path=None):
        if not path:
            path = self.dir_path
        return os.path.join(path, self.cfg_dir_name, self.file)

    def get_config_path(self, mode='find'):
        for path in self.config_paths[os.name]:
            full_path = self.get_full_path(path)
            if os.path.isfile(full_path):
                if os.access(full_path, os.R_OK):
                    self.dir_path = path
                    return True
            else:
                if mode == 'create' and os.access(path, os.W_OK):
                    self.dir_path = path
                    self.generate_config()
                    return True
        else:
            if mode == 'find':
                return self.get_config_path('create')
            else:
                raise RuntimeError("Can't find or write config")

    def import_config(self):
        if self.dir_path:
            if not os.path.isfile(self.get_full_path()):
                self.generate_config()
        else:
            self.get_config_path()
        with open(self.get_full_path(), 'r', encoding='utf-8') as f:
            load_config_data = json.loads(f.read())
        need_update = False
        for key in self.std_config:
            if key not in load_config_data:
                load_config_data[key] = self.std_config[key]
                need_update = True
        if need_update:
            self.update_config(load_config_data)
        print(f'Imported config from: {self.get_full_path()}')
        return load_config_data

    def update_config(self, c_data):
        with open(self.get_full_path(), 'w', encoding='utf-8') as f:
            f.write(json.dumps(c_data, indent=4, sort_keys=self.sort_keys))

    def generate_config(self):
        full_path = self.get_full_path()
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(self.std_config, indent=4, sort_keys=self.sort_keys))
        print(f'Created new config: {full_path}')
