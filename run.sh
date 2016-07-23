#!/usr/bin/env bash

if [ ! -d "Robotenv" ]; then
  virtualenv Robotenv
fi

. Robotenv/bin/activate
pip install --upgrade pip

pip install -r requirements.txt

# pass all arguments onto the "real" script
python RobotRun.py "$@"