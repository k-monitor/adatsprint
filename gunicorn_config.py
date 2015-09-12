"""
Gunicorn settings for the production server
"""
import multiprocessing
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

bind = "127.0.0.1:9876"
workers = multiprocessing.cpu_count() * 2 + 1
daemon = True
raw_env = ['DJANGO_SETTINGS_MODULE=adatsprint.settings_prod']
pidfile = os.path.join(BASE_DIR, 'adatsprint.pid')
accesslog = os.path.join(BASE_DIR, 'adatsprint-access.log')
errorlog = os.path.join(BASE_DIR, 'adatsprint-error.log')
proc_name = 'adatsprint-web'
