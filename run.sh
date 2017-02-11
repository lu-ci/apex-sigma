#!/usr/bin/env bash

# Don't let CDPATH interfere with the cd command
unset CDPATH

# The bot directory, overwrite with SIGMA_HOME
sigma_dir="${SIGMA_HOME:-$HOME/apex-sigma}"

# Make sure we are in the correct working directory
cd "$sigma_dir"

# Execute the bot
exec python3.6 run.py
