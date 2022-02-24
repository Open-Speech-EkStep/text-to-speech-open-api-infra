import subprocess
from scripts.utilities import cmd_runner


def append_config(command, enable_gpu, node_name, replica_count, gpu_count=None, cpu_count=None,
                  cuda_visible_devices=None,
                  node_selector_accelerator=None):
    if node_selector_accelerator:
        command = "{} --set nodeSelector.accelerator='{}'".format(command, node_selector_accelerator)

    cpu_command = "--set resources.requests.cpu='{}' --set env.gpu='{}'".format(cpu_count, False)
    if replica_count is not None:
        command = f"{command} --set replicaCount={replica_count}"
    if node_name:
        command = "{} --set nodeSelector.\"kubernetes\.io/hostname\"={}".format(command, node_name)
    if enable_gpu:
        gpu_command = "--set resources.limits.\"nvidia\.com/gpu\"='{}' --set env.gpu='{}'".format(
            gpu_count, enable_gpu)
        command = "{} {}".format(command, gpu_command)
        if cuda_visible_devices:
            command = '{} --set env.CUDA_VISIBLE_DEVICES="{}"'.format(gpu_command, cuda_visible_devices)
    else:
        command = "{} {}".format(command, cpu_command)
    return command


class LanguageConfig:

    def __init__(self, language_code, base_name, helm_chart_path):
        self.language_code = language_code
        self.helm_chart_path = helm_chart_path
        self.release_name = "{}-{}".format(base_name, language_code).replace('_', '-')
        print("Release name", self.release_name)

    def is_deployed(self, namespace):
        result = subprocess.getoutput('helm status {} -n {} --output yaml'.format(self.release_name, namespace))
        if "release: not found" in result.lower():
            return False
        else:
            return True

    def get_language_code(self):
        return self.language_code

    def get_language_code_as_list(self):
        return [self.language_code]

    def deploy(self, namespace, api_changed, gpu_count, enable_gpu, cpu_count, image_name,
               image_version, node_selector_accelerator, replica_count, cuda_visible_devices, node_name=None):
        is_deployed = self.is_deployed(namespace)
        print("IS_DEPLOYED", is_deployed)
        if is_deployed == True:
            process = "upgrade"
            if api_changed == True:
                uninstall_command = "helm uninstall {0} --namespace {1}".format(self.release_name,
                                                                                namespace)
                cmd_runner(uninstall_command, "LANGUAGE :" + self.language_code)
                process = "install"
        else:
            process = "install"

        pull_policy = "Always" if api_changed == True else "IfNotPresent"

        command = "helm {0} --timeout 180s {1} {2} --namespace {3} --set env.languages='[\"{4}\"]' --set " \
                  "image.pullPolicy='{5}' --set image.repository='{6}' --set image.tag='{7}'".format(
            process, self.release_name, self.helm_chart_path, namespace, self.language_code,
            pull_policy, image_name,
            image_version)

        command = append_config(command, enable_gpu, node_name, replica_count, gpu_count, cpu_count,
                                cuda_visible_devices,
                                node_selector_accelerator)
        # print(command)
        cmd_runner(command, "LANGUAGE :" + self.language_code)


class MultiLanguageConfig:

    def __init__(self, language_code_list, base_name, helm_chart_path):
        self.language_code_list = language_code_list
        self.helm_chart_path = helm_chart_path
        self.languages_codes_string = "-".join(language_code_list)
        self.release_name = "{}-{}".format(base_name, self.languages_codes_string).replace('_', '-')
        print("Release name", self.release_name)

    def is_deployed(self, namespace):
        result = subprocess.getoutput('helm status {} -n {} --output yaml'.format(self.release_name, namespace))
        if "release: not found" in result.lower():
            return False
        else:
            return True

    def get_language_code(self):
        return self.languages_codes_string

    def get_language_code_as_list(self):
        return self.language_code_list

    def deploy(self, namespace, api_changed, gpu_count, enable_gpu, cpu_count, image_name,
               image_version, node_selector_accelerator, replica_count, cuda_visible_devices, node_name=None):
        if len(self.language_code_list) == 0:
            raise ValueError("No Language codes present.Please add language codes or remove the item from list")

        is_deployed = self.is_deployed(namespace)
        print("IS_DEPLOYED", is_deployed)
        if is_deployed == True:
            process = "upgrade"
            if api_changed == True:
                uninstall_command = "helm uninstall {0} --namespace {1}".format(self.release_name, namespace)
                cmd_runner(uninstall_command, "LANGUAGE :" + ",".join(self.language_code_list))
                process = "install"
        else:
            process = "install"

        pull_policy = "Always" if api_changed == True else "IfNotPresent"

        languages = ["\"{}\"".format(x) for x in self.language_code_list]
        languages = "\,".join(languages)
        command = "helm {0} --timeout 180s {1} {2} --namespace {3} --set env.languages='[{4}]' --set " \
                  "image.pullPolicy='{5}' --set image.repository='{6}' --set image.tag='{7}'".format(
            process, self.release_name, self.helm_chart_path, namespace, languages, pull_policy, image_name,
            image_version)

        command = append_config(command, enable_gpu, node_name, replica_count, gpu_count, cpu_count,
                                cuda_visible_devices,
                                node_selector_accelerator)

        # print(command)
        cmd_runner(command, "LANGUAGE :" + ",".join(self.language_code_list))
