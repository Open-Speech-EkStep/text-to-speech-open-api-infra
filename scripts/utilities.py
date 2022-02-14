import subprocess
from collections import OrderedDict
import yaml


def parse_boolean_string(value):
    if value == 'true':
        return True
    else:
        return False


def ordered_load(stream, Loader=yaml.SafeLoader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def ordered_dump(data, stream=None, Dumper=yaml.SafeDumper, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


def cmd_runner(command, caller):
    print(command, caller)
    result = subprocess.run(command, shell=True, capture_output=True)
    if result.stderr:
        print("Error:", result.stderr)
    if result.stdout:
        print("Helm => ", caller, " Out => ", result.stdout.decode('utf-8'), "\n")


def write_to_yaml(config, path):
    with open(path, "w") as file:
        try:
            ordered_dump(config, stream=file, Dumper=yaml.SafeDumper)
        except yaml.YAMLError as exc:
            print("Error: ", exc)


def read_config_yaml(config_path):
    with open(config_path, "r") as stream:
        try:
            config = ordered_load(stream, yaml.SafeLoader)
            return config
        except yaml.YAMLError as exc:
            print("Error: ", exc)
            return None
