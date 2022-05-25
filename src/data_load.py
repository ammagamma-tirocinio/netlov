import yaml
import pickle
from config import *


def pickle_load(path):
    print('start loading pickle file...')
    with open(path, 'rb') as f:
        data = pickle.load(f)
    print('file loaded')
    return data

def yaml_load(path):
    print('start loading yaml file')
    with open(path, 'r') as f:
        map_col = yaml.load(f,Loader=yaml.FullLoader)
    print('file loaded')
    return map_col



