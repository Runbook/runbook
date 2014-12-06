#!/bin/bash
# start rethinkdb, redis and web in tmux panes
tmux new -s 'web_db' -d 'python src/web/web.py instance/web.cfg.default'
tmux split-window -v 'redis-server'
tmux split-window -h 'rethinkdb'
tmux attach -t 'web_db'
