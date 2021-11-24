pipeline {
    agent {
        label: 'slave01'
    }

    stages{
        stage("global") {
            steps {
                sh 'hello world!'
            }
        }
        stage('test branch') {
            when {
                branch 'test'
            }
            steps {
                sh 'I am in branch test'
            }
        }
        stage('master') {
            when {
                branch 'master'
            }
            steps {
                sh 'I am in master'
            }
        }
    }
}