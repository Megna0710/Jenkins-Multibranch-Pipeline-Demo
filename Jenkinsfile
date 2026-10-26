pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        APP_NAME = 'jenkins-multibranch-demo'
        PACKAGE_DIR = 'dist'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Building branch: ${env.BRANCH_NAME ?: 'manual'}"
                checkout scm
                sh 'git rev-parse --short HEAD'
            }
        }

        stage('Compile') {
            steps {
                sh 'python --version'
                sh 'python -m compileall -q app tests'
            }
        }

        stage('Review') {
            steps {
                sh 'python scripts/review.py'
            }
        }

        stage('Test') {
            steps {
                sh 'python -m unittest discover -s tests -p "test_*.py" -v'
            }
        }

        stage('Package') {
            steps {
                sh '''
                    set -eu
                    rm -rf "$PACKAGE_DIR"
                    mkdir -p "$PACKAGE_DIR"
                    cp -R app "$PACKAGE_DIR/app"
                    cp README.md "$PACKAGE_DIR/README.md"
                    tar -czf "$PACKAGE_DIR/${APP_NAME}-${BUILD_NUMBER}.tar.gz" -C "$PACKAGE_DIR" app README.md
                    sha256sum "$PACKAGE_DIR/${APP_NAME}-${BUILD_NUMBER}.tar.gz" > "$PACKAGE_DIR/checksum.sha256"
                '''
                archiveArtifacts artifacts: 'dist/*', fingerprint: true
            }
        }

        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    branch 'master'
                }
            }
            steps {
                echo 'Deploy stage: publishing the validated build artifact to the Jenkins workspace.'
                sh '''
                    set -eu
                    mkdir -p deployment
                    cp "$PACKAGE_DIR/${APP_NAME}-${BUILD_NUMBER}.tar.gz" deployment/
                    cp "$PACKAGE_DIR/checksum.sha256" deployment/
                    printf 'branch=%s\nbuild=%s\ncommit=%s\n' "$BRANCH_NAME" "$BUILD_NUMBER" "$(git rev-parse --short HEAD)" > deployment/release-info.txt
                '''
                archiveArtifacts artifacts: 'deployment/*', fingerprint: true
            }
        }
    }

    post {
        always {
            echo "Pipeline finished for ${env.BRANCH_NAME ?: 'manual'} with status: ${currentBuild.currentResult}"
        }
        success {
            echo 'All applicable stages completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Review the stage logs before merging or deploying.'
        }
    }
}
