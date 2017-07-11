import os

os.system("gunicorn -w 4 webserver:app --log-file -")