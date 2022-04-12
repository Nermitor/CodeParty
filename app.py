from flask import Flask

from apps.authorization import app as auth_app
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex-lyceum-secret-key'
app.config['SECURITY_PASSWORD_SALT'] = 'my_precious_two'

if __name__ == '__main__':
    db_session.global_init("db/db.db")
    app.register_blueprint(auth_app.authorisation)
    app.run()
