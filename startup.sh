#!/usr/bin/env bash
sudo pkill -f handler 
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
sudo python "$DIR/handler.py" &
scratch --document "$DIR/default.sb"