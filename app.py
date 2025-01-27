from flask import Flask
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config.from_object('config.Config')

scheduler = APScheduler()
scheduler.init_app(app)