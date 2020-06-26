import abc
from typing import Union, List

import peewee

from app.database import models
from app.database.setup import db
from app.entities import dto, errors


class MessageService(abc.ABC):
    @abc.abstractmethod
    def get_one(self, user_id: str, message_id: str) -> Union[None, dto.ReceivedMessage]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, user_id: str, message_id: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def create(self, user_id: str, message_dto: dto.Message) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self, user_id: str, is_read: bool) -> List[dto.ReceivedMessage]:
        raise NotImplementedError


# Usually I'd inject the db connection here (so it will be testable).
# But the library is pretty generic and you can use in-memory db for testing
# However, in case I'd have to use some NoSQL db, I'd implement a new User class with other ORM
class MessageSQLService(MessageService):
    def get_one(self, user_id: str, message_id: str) -> Union[None, dto.ReceivedMessage]:
        with db:
            receiver = models.Receiver.get_or_none(
                models.Receiver.message == message_id and user_id == models.Receiver.receiver)
            if receiver:
                receiver.is_read = True
                receiver.save()
                query_res = models.Receiver.select(models.Message.subject,
                                                   models.Message.content,
                                                   models.Message.creation_date,
                                                   models.Receiver.receiver_id,
                                                   models.Receiver.is_read,
                                                   models.Sender.sender_id).where(
                    models.Receiver.receiver == user_id).join(
                    models.Message).where(
                    models.Message.id == message_id).join(
                    models.Sender).first()

                return dto.ReceivedMessage(sender_id=query_res.message.sender.sender_id,
                                           receiver_id=query_res.receiver_id,
                                           content=query_res.message.content,
                                           subject=query_res.message.subject,
                                           is_read=query_res.is_read,
                                           creation_date=query_res.message.creation_date
                                           )

            return None

    def delete(self, user_id: str, message_id: str) -> bool:
        has_delete_occurred = False

        with db:
            receiver: models.Receiver = models.Receiver.get_or_none(
                models.Receiver.message == message_id and models.Receiver.receiver == user_id)
            if receiver:
                receiver.delete().execute()
                has_delete_occurred = True
            else:
                sender = models.Sender.get_or_none(
                    models.Sender.message == message_id and models.Sender.sender == user_id)
                if sender:
                    sender.delete().execute()
                    has_delete_occurred = True

            user_has_message = models.Receiver.get_or_none(models.Receiver.message == message_id) or models.Sender.get_or_none(
                    models.Sender.message == message_id)

            if not user_has_message:
                message = models.Message.get_or_none(models.Message.id == message_id)
                if message:
                    message.delete().execute()

            return has_delete_occurred

    def create(self, user_id: str, message_dto: dto.Message) -> str:
        if message_dto.sender_id != user_id:
            raise errors.UnauthorizedWriteMessage()

        with db:
            if not models.User.get_or_none(models.User.id == message_dto.sender_id):
                raise errors.SenderNotFound()

            if not models.User.get_or_none(models.User.id == message_dto.receiver_id):
                raise errors.ReceiverNotFound()

            with db.atomic() as message_transaction:
                try:
                    message = models.Message(subject=message_dto.subject,
                                             content=message_dto.content)
                    message.save(force_insert=True)

                    models.Sender(sender_id=message_dto.sender_id,
                                  message_id=message.id).save(force_insert=True)
                    models.Receiver(receiver_id=message_dto.receiver_id,
                                    message_id=message.id).save(force_insert=True)

                    return message.id
                except peewee.PeeweeException:
                    message_transaction.rollback()
                    raise errors.ApiError("Unexpected error occurred while trying to send the message")

    def get_all(self, user_id: str, is_read: bool) -> List[dto.ReceivedMessage]:
        with db:
            receiver = models.Receiver.get_or_none(models.Receiver.receiver == user_id)
            if receiver:
                all_messages = models.Receiver.select(models.Message.subject,
                                                      models.Message.content,
                                                      models.Message.creation_date,
                                                      models.Receiver.receiver_id,
                                                      models.Receiver.is_read,
                                                      models.Sender.sender_id).where(
                    models.Receiver.receiver == user_id).join(
                    models.Message).where(
                    models.Message.id == models.Receiver.message).join(
                    models.Sender)

                if is_read is None:
                    return [dto.ReceivedMessage(sender_id=m.message.sender.sender_id,
                                                receiver_id=m.receiver_id,
                                                content=m.message.content,
                                                subject=m.message.subject,
                                                is_read=m.is_read,
                                                creation_date=m.message.creation_date
                                                ) for m in all_messages.execute()]
                else:
                    filtered_messages = all_messages.where(models.Receiver.is_read == is_read).execute()
                    return [dto.ReceivedMessage(sender_id=m.message.sender.sender_id,
                                                receiver_id=m.receiver_id,
                                                content=m.message.content,
                                                subject=m.message.subject,
                                                is_read=m.is_read,
                                                creation_date=m.message.creation_date
                                                ) for m in filtered_messages]

            return []
