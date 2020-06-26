from peewee import SqliteDatabase, Database

from config import conf


class DBFactory:
    _databases = {
        'sqlite': SqliteDatabase
    }

    @staticmethod
    def create(db_type, db_name) -> Database:
        selected_db = DBFactory._databases.get(db_type)(db_name)
        if not selected_db:
            raise KeyError("Database was not found")

        return selected_db


db: Database = DBFactory.create(conf.DB_TYPE, conf.DB_NAME)


def initialize():
    from app.database.models import Message, User, Sender, Receiver, Status

    db.drop_tables([Message, User, Sender, Receiver, Status])
    db.create_tables([Message, User, Sender, Receiver, Status])

