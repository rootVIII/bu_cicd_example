from os import mkdir
from os.path import realpath, basename, isdir
from yaml import safe_load


class AppConfig:
    def __init__(self):
        root = realpath(__file__)[:-len(basename(__file__))][:-7]

        with open(root + 'resources/config.yaml') as yaml_in:
            self.config = safe_load(yaml_in)

        if not isdir(self.config['file_store']):
            mkdir(self.config['file_store'])

        log_dir = self.config['log_path'][:-len(basename(self.config['log_path']))]
        if not isdir(log_dir):
            mkdir(log_dir)

    def retrieve_environment(self):
        return self.config
