import os

from flask_bootstrap import Bootstrap
from flask import Flask

from dotenv import load_dotenv

load_dotenv()
from routes import simple_page

app = Flask(__name__)
app.register_blueprint(simple_page)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
Bootstrap(app)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
