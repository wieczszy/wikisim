from flask import Flask

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'you-will-never-guess'

from app import routes