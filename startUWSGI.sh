#!/bin/bash
DIR=/media/GIT-private/gogs/ytdjango/ytdjango
MP3_DIR=/media/GIT-private/gogs/ytdjango/ytdjango/out_dir/
LISTEN_IP=127.0.0.1
#if [ ! -e $DIR/venv ] ; then
#        virtualenv $DIR/venv
#fi
killall -9 uwsgi
#source $DIR/venv/bin/activate
#pip install -r $DIR/requierments.txt
pip install uwsgi
uwsgi --http $LISTEN_IP:8000 --chdir $DIR --wsgi-file $DIR/ytdjango.wsgi --master --processes 1 --workers 1 --threads 1 --daemonize=$DIR/ytdjango_LOG.txt  --static-map /static=$DIR/website/static --static-map /mp3=$MP#_DIR
