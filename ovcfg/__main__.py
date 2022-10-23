from ovcfg import Config

print('[WARNING] This functional only for testing. In runtime you have to use this only as module for you scripts')
input('Press Enter to create config')
sc = {
    'first': 'first param',
    'second': 'second param',
}
cfg = Config(sc, 'ex.json').import_config()
print(cfg)
