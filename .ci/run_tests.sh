#!/usr/bin/env bash

echo 'Starting Travis build testing...'
#nosetests --with-coverage
echo 'Copying config'
cp config_example.py config.py
echo 'Launching Sigma'
python run.py
echo 'Sigma Launched And Tested'
echo 'Done Testing'
