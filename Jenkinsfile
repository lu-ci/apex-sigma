node('master') {
    // BUILD
    stage 'Build'
    checkout scm

    env.WORKSPACE = pwd()
    bat .ci/jenkins.bat

    // TEST
    stage 'Test'
    bat 'echo "does nothing right now"'
}