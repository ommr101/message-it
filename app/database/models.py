import uuid
from datetime import datetime

from flask_bcrypt import generate_password_hash, check_password_hash
from peewee import Model, TextField, DateTimeField, ForeignKeyField, BooleanField, IntegerField, FloatField

from app.database.setup import db


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id: str = TextField(default=lambda: str(uuid.uuid4()), primary_key=True)
    username: str = TextField(unique=True)
    password: str = TextField()

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Message(BaseModel):
    id = TextField(default=lambda: str(uuid.uuid4()), primary_key=True)
    subject: str = TextField()
    content: str = TextField()
    creation_date: datetime = DateTimeField(default=datetime.now())


class Sender(BaseModel):
    id = TextField(default=lambda: str(uuid.uuid4()), primary_key=True)
    sender = ForeignKeyField(User)
    message = ForeignKeyField(Message)


class Receiver(BaseModel):
    id = TextField(default=lambda: str(uuid.uuid4()), primary_key=True)
    receiver = ForeignKeyField(User)
    message = ForeignKeyField(Message)
    is_read = BooleanField(default=False)


class Status(BaseModel):
    endpoint: str = TextField(primary_key=True)
    counter: int = IntegerField(default=0)
    avg_time: float = FloatField(default=0)
