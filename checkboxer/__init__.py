from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

'''
Приложение позволяет создавать чек листы, использовать готовые, делиться чеклистами
'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'DFSDSDFSDFFSDF'
app.config.from_object(Config)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)


from checkboxer import routes, models