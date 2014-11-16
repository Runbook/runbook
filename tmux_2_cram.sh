#!/bin/bash
# start crAM control, broker and worker in tmux
cd src/cram
tmux new -s 'cram' -d 'python control.py config/control.yml.default'
tmux split-window -v 'python broker.py config/main.yml.default'
tmux split-window -v 'python worker.py config/main.yml.default'
tmux attach -t 'cram'
