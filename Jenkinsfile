def name = "affinitic.smartweb"

pipeline {
  agent none
  stages {
    stage('Build') {
      parallel {
        stage('Build on Plone 6.0') {
          agent any
          steps {
            script {
              new be.affinitic.Plone().buildTest(name, '6.0')
            }
          }
        }
      }
    }
    stage('Test') {
      parallel {
        stage('Test on Plone 6.0') {
          agent any
          steps {
            script {
              new be.affinitic.Plone().testing('6.0')
            }
          }
          post {
            always {
              step([
                $class: 'JUnitResultArchiver',
                testResults: 'testreports-6.0/*.xml'
              ])
            }
          }
        }
      }
    }
  }
  
  post {
    success {
      script {
        new be.affinitic.Mattermost().send('SUCCESS')
      }
    }
    failure {
      script {
        new be.affinitic.Mattermost().send('FAILURE')
      }
    }
    unstable {
      script {
        new be.affinitic.Mattermost().send('UNSTABLE')
      }
    }
  }
}
