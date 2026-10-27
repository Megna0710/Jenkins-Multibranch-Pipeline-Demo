
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
                bat 'git rev-parse --short HEAD'
            }
        }

        stage('Compile') {
            steps {
                bat 'python --version'
                bat 'python -m compileall -q app tests'
            }
        }

        stage('Review') {
            steps {
                bat 'python scripts/review.py'
            }
        }

        stage('Test') {
            steps {
                bat 'python -m unittest discover -s tests -p "test_*.py" -v'
            }
        }

        stage('Package') {
            steps {
                bat '''
                    if exist "%PACKAGE_DIR%" rmdir /s /q "%PACKAGE_DIR%"
                    mkdir "%PACKAGE_DIR%"
                    xcopy app "%PACKAGE_DIR%\\app\\" /E /I /Q /Y
                    if errorlevel 1 exit /b 1
                    copy README.md "%PACKAGE_DIR%\\README.md"
                    if errorlevel 1 exit /b 1
                    tar -czf "%PACKAGE_DIR%\\%APP_NAME%-%BUILD_NUMBER%.tar.gz" -C "%PACKAGE_DIR%" app README.md
                    if errorlevel 1 exit /b 1
                    certutil -hashfile "%PACKAGE_DIR%\\%APP_NAME%-%BUILD_NUMBER%.tar.gz" SHA256 > "%PACKAGE_DIR%\\checksum.sha256"
                    if errorlevel 1 exit /b 1
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
                bat '''
                    if not exist deployment mkdir deployment
                    copy "%PACKAGE_DIR%\\%APP_NAME%-%BUILD_NUMBER%.tar.gz" deployment\\
                    if errorlevel 1 exit /b 1
                    copy "%PACKAGE_DIR%\\checksum.sha256" deployment\\
                    if errorlevel 1 exit /b 1
                    (
                        echo branch=%BRANCH_NAME%
                        echo build=%BUILD_NUMBER%
                        for /f %%C in ('git rev-parse --short HEAD') do echo commit=%%C
                    ) > deployment\\release-info.txt
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
