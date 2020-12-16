import logging
from json import load, dump
from os import listdir
from uuid import uuid4
from common.config import config


def get_logger(name):
    log_format = '%(asctime)s.%(msecs)03d %(levelname)5s  %(message)8s'
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                        format=log_format, filemode='a',
                        filename=config['log_path'])

    console = logging.FileHandler(config['log_path'])
    console.setLevel(logging.CRITICAL)
    console.setFormatter(logging.Formatter(log_format))
    logging.getLogger(name).addHandler(console)
    return logging.getLogger(name)


def get_file_contents(file_name):
    if file_name not in listdir(config['file_store']):
        raise Exception('Error %s does not exist' % file_name)
    with open(config['file_store'] + file_name) as json_file:
        return load(json_file)


def write_json(name, json_data):
    with open(config['file_store'] + name, 'w') as json_file:
        dump(json_data, json_file)


def make_file_name():
    return str(uuid4()).replace('-', '')
