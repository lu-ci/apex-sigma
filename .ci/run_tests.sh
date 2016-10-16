#!/usr/bin/env bash

echo 'Starting Travis build testing...'
#nosetests --with-coverage
echo 'Launching Sigma'
python sigma.py
echo 'Sigma Launched'
