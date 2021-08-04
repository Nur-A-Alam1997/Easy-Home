
from EasyHome import app

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = "Easyhome_db"

# mysql = MySQL(app)

# APP_ROOT = os.path.dirname(os.path.abspath(__file__))
# jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
