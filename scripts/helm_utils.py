from scripts.utilities import cmd_runner, ordered_load
import subprocess
import yaml


def get_releases(base_name, namespace):
    result = subprocess.getoutput('helm list -f "^{}-(.*)" -n {} -o yaml'.format(base_name, namespace))
    result = result[result.index("- app_version"):]
    release_list = ordered_load(result, yaml.SafeLoader)
    return [release["name"] for release in release_list if
            release["name"] != "{}-envoy".format(base_name) and release["name"] != "{}-proxy".format(base_name)]


def uninstall_release(release, namespace):
    command = "helm uninstall {} -n {}".format(release, namespace)
    cmd_runner(command, "Remove: {}".format(release))


def remove_unwanted_releases(new_releases, existing_releases, namespace):
    removed_releases = []
    for release in existing_releases:
        if release not in new_releases:
            uninstall_release(release, namespace)
            removed_releases.append(release)
    return removed_releases
