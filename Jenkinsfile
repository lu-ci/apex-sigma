node('master') {
    // BUILD
    stage 'Build'
    
    env.WORKSPACE = pwd()
    
    bat 'virtualenv --python=python35 sigma.env'
    bat 'sigma.venv/Scripts/activate'
    bat 'pip install -r requirements.txt'
    
    // TEST
    stage 'Test'
    bat 'echo "does nothing right now"'
}