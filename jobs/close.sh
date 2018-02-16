#!/bin/bash

cd /var/lib/jenkins/scripts/workbench_scripts/
python ./job_manager.py -f "$1" -a "$2" -c "$3"
echo "DONE!"
