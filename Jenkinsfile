pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'docker built -t example .'
      }
    }
    stage('Tests') {
      steps {
        sleep 5
      }
    }
    stage('Approval') {
      steps {
        input 'Você aprova para deploy?'
      }
    }
    stage('Deploy') {
      steps {
        sh 'echo "fazendo deploy"'
      }
    }
  }
}