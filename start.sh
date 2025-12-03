#!/bin/bash

script_path="$(cd "$(dirname "$0")" && pwd)"
python_main="$script_path/main.py"

screen -dmS python_management python3 "$python_main"
exit