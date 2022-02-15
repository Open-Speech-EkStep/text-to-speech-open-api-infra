## Text-to-speech-open-api-infra:

### Step 1: Install Helm

To install helm in linux, Run the following: 
```commandline
    sh install_helm.sh
```

To install helm in mac, Run the following:
```commandline
    brew install helm   
```

### Step 2: Install python dependencies

    Install python >= 3.7

    Run : `pip install requirements.txt`

### Step 3: Configure aws eks configuration to kubeconfig:

Run `aws eks --region <region-name> update-kubeconfig --name <cluster-name>`

### Step 4: Pre-requisites in k8s

Create a namespace using the following command: `kubectl create namespace <namespace-name>`


### Step 5: Install helm charts in k8s


To deploy Run the following command:
```commandline
python deploy.py --namespace namespace-name --image-name gcr.io/ekstepspeechrecognition/text_to_speech_open_api --image-version 2.1.15 --api-updated true
```

### Step 6: To deploy nginx, Run the following:

```
kubectl apply -f infra/nginx/nginx.yaml -n <namespace-name>
```