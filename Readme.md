# Text to Speech Open Api Infra

This repo helps deploy our TTS services on different infra platforms. We use helm charts to deploy our components.

TTS API Documentation: https://open-speech-ekstep.github.io/tts_model_api/

Deployment Guide: https://open-speech-ekstep.github.io/api_deployment/


| Branch       | Purpose                           |
|--------------|-----------------------------------|
| azure-deploy | Deployment on Azure AKS           |
| aws-deploy   | Deployment on AWS EKS             |

You can fork the branch closer to your infra and built on top of it. For the details of TTS deployment look at [TTS API repo](https://github.com/Open-Speech-EkStep/text-to-speech-open-api).

#### infra directories

| Directory          | Purpose                                                                                 |
|--------------------|-----------------------------------------------------------------------------------------|
| infra/tts-model-v1 | Scripts and helm charts for model pods.                                                 |
| infra/envoy        | Scripts and helm charts for envoy to support routing and load distribution across pods. |


Below are the details for some files that you need to know to start with this.

#### app_config.yaml

This is main file to define the cluster of languages you want to have in one single pod. It supports few more parameters as mentioned below.

```yaml
base_name: tts-model-v1 # base name for the pod.
config:
  - languages:
      - en # languages to be deployed in the pod.
    gpu:
      count: 0
      accelerator: 'nvidia-A100' # (Optional) gpu accelerator parameter.
      CUDA_VISIBLE_DEVICES: "2" # (Optional) index of the GPU exposed.
    replicaCount: 3 # (Optional)
    nodeName: "scn32-100g" # (Optional) node selector name.
  - languages:
      - ne
      - doi
    gpu:
      count: 0
      accelerator: 'nvidia-A100'
      CUDA_VISIBLE_DEVICES: "1"
    nodeName: "scn32-100g"
```



#### deploy.py

We have created a python script to dynamically generate all the deployments as the cluster config changes.


#### Jenkinsfile

Jenkins config file.

#### Running it on local

```shell
python3 deploy.py --namespace <namespace> --api-updated <boolean value> --enable-ingress <enable ingress for envoy admin> --image-name <model image> --image-version <docker image version> --enable-envoy-admin <deploy envoy admin component>
```

Example:

```shell
python3 deploy.py --namespace stage --api-updated true --enable-ingress false --image-name gcr.io/ekstepspeechrecognition/text_to_speech_open_api --image-version 2.1.21 --enable-envoy-admin true
```

Documentation Reference:
TTS Repo https://github.com/Open-Speech-EkStep/text-to-speech-open-api.

Developer Guide https://open-speech-ekstep.github.io/tts_model_api/
