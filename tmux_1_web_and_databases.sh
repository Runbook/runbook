#!/bin/bash
# start rethinkdb, redis and web in tmux panes
tmux new -s 'web_db' -d 'python src/crweb/web.py instance/crweb.cfg.default'
tmux split-window -v 'redis-server'
tmux split-window -h 'rethinkdb'
tmux attach -t 'web_db'
