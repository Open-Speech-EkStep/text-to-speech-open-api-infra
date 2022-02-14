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
                            )
                        ])
                    ])
                }
            }
        }
        stage("Deploy tts service") {
            steps {
                    sh "kubectl get pods -n nltm"
                    sh "python3 deploy.py --namespace $params.NAMESPACE --api-updated $params.API_UPDATED --image-name $params.IMAGE_NAME --image-version $params.IMAGE_VERSION"
            }
        }
    }
}
