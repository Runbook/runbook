#!/bin/bash
# start crBridge bridge, broker and actioner in tmux
cd src/crbridge
tmux new -s 'crbridge' -d 'python bridge.py config/config.yml.default'
tmux split-window -v 'python broker.py config/config.yml.default'
tmux split-window -v 'python actioner.py config/config.yml.default'
tmux attach -t 'crbridge'
