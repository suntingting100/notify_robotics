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
                wrap([$class: 'BuildUser']) {
                    env.USER_ID = env.CHANGE_AUTHOR
                }
                println env.USER_ID
                def result = currentBuild.getResult()
                env.STATUS=result
                def duration_time = currentBuild.getDuration()/1000
                env.DURATION_TIME = duration_time
                sh '''curl --location --request POST \'http://10.20.17.124:8888/buildResult\' \\
                    --header \'Content-Type: application/json\' \\
                    --data \'
                    {
                      "line": "TEST",
                      "user": "'"${USER_ID}"'",
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
                        "build_result": "${STATUS}",
                        "duration_time": "'${DURATION_TIME}'",
                        "artifact": "'${RUN_ARTIFACTS_DISPLAY_URL}'",
                        "test_report": "'${RUN_DISPLAY_URL}'"
                      }
                    }\''''
            }

        }
    }
}
