pipeline {
    agent any

    stages {
        stage('Setup parameters') {
            steps{
                script {
                    properties([
                        parameters([
                            booleanParam(
                                defaultValue: true,
                                name: 'API_UPDATED'
                            ),
                            string(
                                defaultValue: 'stage',
                                name: 'NAMESPACE'
                            ),
                            string(
                                defaultValue: 'gcr.io/ekstepspeechrecognition/text_to_speech_open_api',
                                name: 'IMAGE_NAME'
                            ),
                            string(
                                defaultValue: '2.1.10',
                                name: 'IMAGE_VERSION'
                            ),
                            booleanParam(
                                defaultValue: true, 
                                name: 'ENABLE_ENVOY_ADMIN'
                            )
                        ])
                    ])
                }
            }
        }
        stage("Deploy") {
            steps {
                sh "chmod +x ./install_helm.sh"
                sh "./install_helm.sh"
                withCredentials([
                    file(credentialsId: 'meity-eks-kube', variable: 'KUBECONFIG'),
                    string(credentialsId: 'meity-eks-iam-access', variable: 'AWS_ACCESS_KEY_ID'),
	                string(credentialsId: 'meity-eks-iam-secret', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh 'python3 -m pip install pyyaml'
                    sh "python3 deploy.py --namespace $params.NAMESPACE --api-updated $params.API_UPDATED --image-name $params.IMAGE_NAME --image-version $params.IMAGE_VERSION --enable-envoy-admin $params.ENABLE_ENVOY_ADMIN"
                }
            }
        }
    }
}
