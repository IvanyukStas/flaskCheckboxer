from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

'''
Приложение позволяет создавать чек листы, использовать готовые, делиться чеклистами
'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'DFSDSDFSDFFSDF'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)


from checkboxer import routes, models