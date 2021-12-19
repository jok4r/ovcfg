import os
import json

config_path = '/etc'
config_path_alternate = os.path.join(os.path.expanduser("~"), '.config')


class Config(object):
    def __init__(self, std_config=None, file='example.cfg', cfg_dir_name='example', dir_path=None):
        if std_config is None:
            std_config = {}
        self.std_config = std_config
        self.file = file
        self.cfg_dir_name = cfg_dir_name
        if dir_path:
            self.dir_path = dir_path
        else:
            self.dir_path = config_path

    def import_config(self):
        full_path = os.path.join(self.dir_path, self.cfg_dir_name, self.file)
        if not os.path.isfile(full_path):
            if self.dir_path == config_path_alternate:
                self.dir_path = config_path
                self.generate_config()
                full_path = os.path.join(self.dir_path, self.cfg_dir_name, self.file)
            else:
                self.dir_path = config_path_alternate
                return self.import_config()
        with open(full_path, 'r') as f:
            load_config_data = json.loads(f.read())
        # self.std_config = self.get_std_config()
        need_update = False
        for key in self.std_config:
            if key not in load_config_data:
                load_config_data[key] = self.std_config[key]
                need_update = True
        if need_update:
            self.update_config(full_path, load_config_data)
        return load_config_data

    @staticmethod
    def update_config(path, c_data):
        with open(path, 'w') as f:
            f.write(json.dumps(c_data, indent=4, sort_keys=True))

    def generate_config(self):
        full_path = os.path.join(self.dir_path, self.cfg_dir_name, self.file)
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(json.dumps(self.std_config, indent=4, sort_keys=True))
        except PermissionError:
            self.dir_path = config_path_alternate
            return self.generate_config()
        print(f'Created new config: {full_path}')


if __name__ == '__main__':
    input('Press Enter to create config')
    sc = {
        'first': 'first param',
        'second': 'second param',
    }
    cfg = Config(sc, 'ex.json').import_config()
    print(cfg)
