# remove the --capture-output flag if you have problems running the backend container (Read the remarks in TTS_Voice.md at assets/docs for more information)
gunicorn -w $WEBWORKERS -b 0.0.0.0:$APIPORT app:app -c gunicorn_conf.py --capture-output
