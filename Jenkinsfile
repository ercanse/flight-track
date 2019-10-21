node {
    stage('Checkout') {
        checkout([
            $class: 'GitSCM',
            branches: [[name: env.BRANCH_NAME]],
            extensions: [[$class: 'WipeWorkspace']],
            userRemoteConfigs: [[credentialsId: 'github-flight-track', url: 'https://github.com/S-Ercan/flight-track.git']]
        ])
    }
}