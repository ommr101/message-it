import app.database.setup
from app.api.setup import messageit_app
from config import conf

if __name__ == '__main__':
    app.database.setup.initialize()
    messageit_app.run(host=conf.HOST, port=conf.PORT)
