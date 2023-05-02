import yaml
import os

def yaml_load(path):
    # check the path
    if not os.path.isfile(path):
        print("[-] Yaml load failed! File not exists: %s" % path)
        exit(-1)
    # parse file in the yaml format.
    with open(path, 'rb') as fp:
        content = yaml.load(fp, Loader=yaml.FullLoader)
    return content