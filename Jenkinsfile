#!groovy
@Library('jenkins-pipeline-libs@master')

import groovy.transform.Field

@Field def hipchatRoom = 'XL AppSec'

pipeline {
    agent none

    environment {
        GRADLE_OPTS = '-XX:MaxPermSize=256m -Xmx1024m  -Djsse.enableSNIExtension=false'
    }

    parameters {
        string(name: 'tag', defaultValue: '8.1.0', description: 'Specify Docker Image Tag i.e. 8.1.0')
        choice(choices: 'Docker-Hub\nXebiaLabs', description: 'Which Docker Registry?', name: 'registry')
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10', artifactDaysToKeepStr: '7', artifactNumToKeepStr: '5'))
        skipDefaultCheckout()
        timeout(time: 1, unit: 'HOURS')
        timestamps()
        ansiColor('xterm')
    }

    stages {
        stage('End-To-End Tests') {

            agent {
                label "linux || xlp"
            }

            environment {
                XL_RELEASE_LICENSE = credentials('xl-release-license')
            }

            tools {
                jdk 'JDK 8u60'
            }

            steps {
                script {
                    try {
                        checkout scm
                        def gradle_command = "./gradlew clean build testEndToEnd -DCHROME_HEADLESS_MODE=true -PxlrLicense=${XL_RELEASE_LICENSE} -Ptag=${params.tag}"
                        if ("${params.registry}" == "XebiaLabs") {
                            gradle_command += " -PxebialabsRegistry"
                        }
                        sh "${gradle_command}"
                        notifyHipChat("End-To-End Testing finished : xlr-weather-plugin", "GREEN")
                    } catch (err) {
                        notifyHipChat("End-To-End Testing Failed : xlr-weather-plugin", "RED")
                        throw err
                    } finally {
                        publishJunit('**/build/**/TEST-*.xml')
                        cleanWs notFailBuild: true
                    }
                }
            }
        }
    }
}

def publishJunit(path) {
    try {
        junit path
    } catch (e) {
        echo "Failed to publish JUnit test report: ${e.getMessage()}"
    }
}

def notifyHipChat(String message, String notificationColor) {
    hipchatSend color: "${notificationColor}", message: """<a href="\${BLUE_OCEAN_URL}">${env.JOB_NAME} ${
        env.BUILD_NUMBER
    }</a> $message""", notify: true, room: hipchatRoom
}