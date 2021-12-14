pipeline {
    agent {
        label 'slave01'
    }
    environment{
        project_name='notify_robot'
    }
    stages{
        stage("global") {
            steps {

                echo 'hello world!'
            }
        }
        stage('test branch') {
            when {
                branch 'test'
            }
            steps {
//                 scmSkip(deleteBuild: true, skipPattern:'.*\\[ci skip\\].*')
                echo 'I am in branch test'

            }
        }
        stage('master') {
            when {
                branch 'master'
            }
            steps {
                echo 'I am in master'
            }
        }
    }
    post("build result notify"){
        always{
            script{
                def author = sh(returnStdout: true, script: "git log -1 --pretty=format:'%an'").trim()
                env.USER = author
                def result = currentBuild.getResult()
                println result
                env.BUILD_STATUS=result
                def duration_time = currentBuild.getDuration()/1000
                env.DURATION_TIME = duration_time
                sh '''curl --location --request POST \'http://10.20.17.124:8888/buildResult\' \\
                    --header \'Content-Type: application/json\' \\
                    --data \'
                    {
                      "line": "TEST",
                      "user": "'"${USER}"'",
                      "department_name": "QA效能机器人-消息群",
                      "project_info": {
                        "project": "'${project_name}'",
                        "branch": "'"${BRANCH_NAME}"'"
                      },
                      "build_info": {
                        "build_job": "'${JOB_NAME}'",
                        "build_number": "'${BUILD_NUMBER}'",
                        "build_url": "'${RUN_DISPLAY_URL}'",
                        "ci": false,
                        "cd": false,
                        "test": false,
                        "build_result": "'${BUILD_STATUS}'",
                        "duration_time": "'${DURATION_TIME}'",
                        "artifact": "'${ARTIFACT}'",
                        "test_report": ""
                      }
                    }\''''
            }

        }
    }
}
