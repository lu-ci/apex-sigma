#!/usr/bin/env bash

echo 'Starting Travis build testing...'
#nosetests --with-coverage
echo 'Launching Sigma'
python run.py
echo 'Sigma Launched'
echo 'Done Testing'
