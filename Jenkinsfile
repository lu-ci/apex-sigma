node('master') {
    // BUILD
    stage 'Build'
    checkout scm
    
    env.WORKSPACE = pwd()
    
    bat 'virtualenv --python=C:/Python35/python.exe sigma.env'
    bat 'sigma.env/Scripts/activate'
    bat 'pip install -r requirements.txt'
    
    // TEST
    stage 'Test'
    bat 'echo "does nothing right now"'
}