pipeline {
    agent {
        label 'slave01'
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
                scmSkip(deleteBuild: true, skipPattern:'.*\\[ci skip\\].*')
                echo 'I am in branch test'
                sh 'exit 0'
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
}
