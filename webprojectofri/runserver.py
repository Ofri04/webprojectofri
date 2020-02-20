"""
This script runs the webprojectofri application using a development server.
"""

from os import environ
from webprojectofri import app

app.secret_key = 'the random string'

app.config['SECRET_KEY'] = 'the random string'    
SECRET_KEY = 'the random string'


if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
