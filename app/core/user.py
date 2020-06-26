import abc

from app.database import models
from app.database.setup import db
from app.entities import dto, errors


class UserService(abc.ABC):
    @abc.abstractmethod
    def create_new(self, user_id: dto.User) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def is_authorized(self, user_credentials: dto.User):
        raise NotImplementedError


# Usually I'd inject the db connection here (so it will be testable).
# But the library is pretty generic and you can use in-memory db for testing
# However, in case I'd have to use some NoSQL db, I'd implement a new User class with other ORM
class UserSQLService(UserService):
    def create_new(self, user: dto.User) -> str:
        with db:
            if models.User.get_or_none(models.User.username == user.username):
                raise errors.UsernameIsTaken()

            new_user = models.User(**user.to_dict())
            new_user.hash_password()
            new_user.save(force_insert=True)

            return new_user.id

    def is_authorized(self, user_credentials: dto.User) -> bool:
        with db:
            user: models.User = models.User.get_or_none(models.User.id == user_credentials.id)

            return user.check_password(user_credentials.password)
