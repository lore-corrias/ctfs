#!/bin/sh

set -ue

for script in ./helpers/*.sh; do
  if [ "$script" != "/path/to/directory/specific-script.sh" ]; then
    if [ ! -x "$script" ]; then
      chmod +x "$script"
    fi
    sh "$script"
  fi
done

# Packages must be installed for last
if [ ! -x "./run-scripts.sh" ]; then
  chmod +x "./run-scripts.sh"
fi
sh "./run-scripts.sh"
