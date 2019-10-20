node {
    stage('Checkout') {
        checkout([
            $class: 'GitSCM',
            branches: scm.branches,
            extensions: scm.extensions + [[$class: 'LocalBranch'], [$class: 'WipeWorkspace']],
            userRemoteConfigs: [[credentialsId: 'github-flight-track', url: 'https://github.com/S-Ercan/flight-track.git']]
        ])
    }
}