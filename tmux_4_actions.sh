#!/bin/bash
# start actioner in tmux
cd src/actions
tmux split-window -v 'python broker.py config/config.yml.default'
tmux split-window -v 'python actioner.py config/config.yml.default'
tmux attach -t 'actions'
