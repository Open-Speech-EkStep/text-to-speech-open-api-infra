import argparse

from scripts.utilities import parse_boolean_string, write_to_yaml, read_config_yaml
from scripts.helm_utils import get_releases, remove_unwanted_releases
from scripts.envoy_config import EnvoyConfig, update_envoy_config
from scripts.language_config import MultiLanguageConfig, LanguageConfig

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--namespace', default='test-v2', help="Namespace to use")
    parser.add_argument('--image-name', help="Model api image name", required=True)
    parser.add_argument('--image-version', help="Model api image version", required=True)
    parser.add_argument('--api-updated', default='false', help="Flag if api has changed")

    args = parser.parse_args()

    image_name = args.image_name
    image_version = args.image_version
    namespace = args.namespace
    api_updated = args.api_updated

    app_config_path = "app_config.yaml"
    envoy_config_path = "infra/envoy/config.yaml"
    language_helm_chart_path = "infra/tts-model-v1"
    envoy_helm_chart_path = "infra/envoy"

    envoy_config = read_config_yaml(envoy_config_path)
    app_config = read_config_yaml(app_config_path)

    # Argparse library parses all parameters as string. Make sure to handle the boolean values

    api_updated = parse_boolean_string(api_updated)

    if envoy_config is None:
        print("Check the envoy config file")
        exit()
    if app_config is None:
        print("Check the app config file")
        exit()

    release_base_name = app_config["base_name"]
    configuration = app_config["config"]

    # existing_releases = get_releases(release_base_name, namespace)

    new_releases = []
    for item in configuration:

        gpu_count = 0
        cpu_count = 2
        enable_gpu = False
        languages = []
        node_selector_accelerator = None
        CUDA_VISIBLE_DEVICES = None
        replica_count = None
        node_name = None
        if "languages" in item:
            languages = item["languages"]
        if "gpu" in item:
            gpu_count = item["gpu"]["count"]
            enable_gpu = True
            node_selector_accelerator = item["gpu"]["accelerator"]
            if "CUDA_VISIBLE_DEVICES" in item["gpu"]:
                CUDA_VISIBLE_DEVICES = item["gpu"]["CUDA_VISIBLE_DEVICES"]
                if CUDA_VISIBLE_DEVICES == "":
                    CUDA_VISIBLE_DEVICES = None
        if "cpu" in item:
            cpu_count = item["cpu"]["count"]
        if "replicaCount" in item:
            replica_count = item["replicaCount"]
            if replica_count == 0:
                replica_count = None

        if "nodeName" in item:
            node_name = item["nodeName"]

        if len(languages) == 0:
            continue
        elif len(languages) == 1:
            language_code = languages[0]
            language_config = LanguageConfig(language_code, release_base_name, language_helm_chart_path)
            language_config.deploy(namespace, api_updated, gpu_count, enable_gpu, cpu_count,
                                   image_name, image_version, node_selector_accelerator, replica_count,
                                   CUDA_VISIBLE_DEVICES, node_name)
            envoy_config = update_envoy_config(envoy_config, language_config)
            new_releases.append(language_config.release_name)
        else:
            language_config = MultiLanguageConfig(languages, release_base_name, language_helm_chart_path)
            language_config.deploy(namespace, api_updated, gpu_count, enable_gpu, cpu_count,
                                   image_name, image_version, node_selector_accelerator, replica_count,
                                   CUDA_VISIBLE_DEVICES, node_name)
            envoy_config = update_envoy_config(envoy_config, language_config)
            new_releases.append(language_config.release_name)

    # remove_unwanted_releases(new_releases, existing_releases, namespace)

    write_to_yaml(envoy_config, envoy_config_path)
    EnvoyConfig(release_base_name, envoy_helm_chart_path).deploy(namespace)
