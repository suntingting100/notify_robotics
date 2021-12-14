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
            sh '''curl --location --request POST \'http://10.20.17.124:8888/buildResult\' \\
                --header \'Content-Type: application/json\' \\
                --data-raw \'
                {
                  "line": "AI",
                  "user": "wei.yang",
                  "department_name": "QA效能机器人-消息群",
                  "project_info": {
                    "project": "ai-stduio",
                    "branch": "master"
                  },
                  "build_info": {
                    "build_job": "string",
                    "build_number": 54,
                    "build_url": "http://www.baidu.com",

                    "ci": true,
                    "cd": true,
                    "test": true,
                    "build_result": "failed",
                    "duration_time": 20,
                    "artifact": "3132",
                    "test_report": "http://www.sina.com"
                  }
                }\''''
            }
        }
    }
}
