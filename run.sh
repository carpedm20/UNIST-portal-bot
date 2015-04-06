#!/bin/sh
if ! test -f $PIDFILE || ! psgrep `cat $PIDFILE`; then
    python portal_bot.py
    # Write PIDFILE
    echo $! >$PIDFILE
fi
