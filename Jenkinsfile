def dockerImage
def projectName = "test_group_notify_robot"
def credentialsId = 'a3428619-6aa7-482d-97b6-72b83c006530'
def docker_registry = "registry.mycyclone.com"


pipeline {
    options { timestamps () }
    agent {label 'aliyun-slave'}
//     environment {
//         image_name = "test_group_notify_robot"
//         docker_registry = "registry.mycyclone.com"
//     }
    stages {
        stage('build images') {
            steps {
                script {
                    dockerImage = docker.build("${docker_registry}/test_project/${projectName}:latest",
                            "--label \"GIT_COMMIT=${env.GIT_COMMIT}\""
                            + " ."
                    )
                }
            }
        }

        stage('Push to docker repository') {
            when {
                branch 'master'
            }
            options { timeout(time: 5, unit: 'MINUTES') }
            steps {
                withDockerRegistry(credentialsId: "${credentialsId}", url: "https://${docker_registry}") {
                    script {
                        dockerImage.push('latest')
                    }
                }
            }
        }
    }
    post {
        always{
            script {
                sh 'docker rmi registry.mycyclone.com/test_project/process_auto_test:latest'

//                 def author = sh(returnStdout: true, script: "git log -1 --pretty=format:'%an'").trim()
//                 env.USER = author
//                 def result = currentBuild.getResult()
//                 println result
//                 env.BUILD_STATUS=result
//                 def duration_time = currentBuild.getDuration()/1000
//                 env.DURATION_TIME = duration_time
//                 sh '''curl --location --request POST \'http://10.20.17.124:8888/buildResult\' \\
//                     --header \'Content-Type: application/json\' \\
//                     --data \'
//                     {
//                       "line": "TEST",
//                       "user": "'"${USER}"'",
//                       "department_name": "QA效能机器人-消息群",
//                       "project_info": {
//                         "project": "'${project_name}'",
//                         "branch": "'"${BRANCH_NAME}"'"
//                       },
//                       "build_info": {
//                         "build_job": "'${JOB_NAME}'",
//                         "build_number": "'${BUILD_NUMBER}'",
//                         "build_url": "'${RUN_DISPLAY_URL}'",
//                         "ci": false,
//                         "cd": false,
//                         "test": false,
//                         "build_result": "'${BUILD_STATUS}'",
//                         "duration_time": "'${DURATION_TIME}'",
//                         "artifact": "'${ARTIFACT}'",
//                         "test_report": ""
//                       }
//                     }\''''
            }
        }
    }
}

