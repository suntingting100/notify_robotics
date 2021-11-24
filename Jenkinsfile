pipeline {
    agent {
        label 'slave01'
    }
    scmSkip(deleteBuild: true, skipPattern:'.*\\[ci skip\\].*')
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
                echo 'I am in branch test'
                sh 'exit -1'
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
