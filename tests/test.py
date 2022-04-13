import os
import unittest
import ovcfg
import random
import string
from uuid import uuid4


class TestMethods(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMethods, self).__init__(*args, **kwargs)

    def test_main(self):
        sc = {'%s_%s' % (i, _get_rnd_string(10)): _get_rnd_string(10) for i in range(10)}
        config_file = '%s.json' % uuid4()
        cfg_dir_name = str(uuid4())
        print("Creating config: %s with dir name: %s" % (config_file, cfg_dir_name))
        print("Config content:", sc)
        cfg_class = ovcfg.Config(std_config=sc, file=config_file, cfg_dir_name=cfg_dir_name)
        cfg = cfg_class.import_config()
        supposed_config_path = os.path.join(cfg_class.dir_path, cfg_dir_name, config_file)
        if os.path.isfile(supposed_config_path):
            if cfg == sc:
                print("Config file found and match with standard config (sc)")
                del_or_not = input('Delete created config? (y/n): ')
                if del_or_not.lower() == 'y':
                    os.remove(supposed_config_path)
                    os.rmdir(os.path.dirname(supposed_config_path))
            else:
                self.fail("Config file NOT found and match with standard config (sc)!")
        else:
            self.fail('File not found in supposed path: %s' % supposed_config_path)


def _get_rnd_string(length=20):
    letters = string.ascii_letters + string.digits
    password = ''.join(random.choice(letters) for i in range(length))
    return password
