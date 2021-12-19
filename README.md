# ovcfg

Simple module for creating your config files and use it in your projects. Configs may store in /etc and user local directory (~/.config).
## Prerequisites

	- Python3.5 or newer

## Installion
$ python3 -m pip install ovcfg<br /><br />
**OR**<br /><br />
$ python3 -m pip install git+https://github.com/jok4r/ovcfg.git

## Usage
```
from ovcfg import Config

default_config = {
        'first': 'first param',
        'second': 'second param',
    }
cfg = Config(default_config, 'config_name_here.json', 'config_dir_name').import_config()
```
Config file in code above will create config with local path *"~/.config/config_dir_name/config_name_here.json"* **OR** */etc/config_dir_name/config_name_here.json* (if have write permissions to /etc)