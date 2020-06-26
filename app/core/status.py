import abc

from app.database import models
from app.database.setup import db
from app.entities import dto


class StatusService(abc.ABC):
    @abc.abstractmethod
    def increment_endpoint(self, endpoint_path: str, exec_time) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_endpoints_status(self) -> dto.RequestsStatus:
        raise NotImplementedError


# Usually I'd inject the db connection here (so it will be testable).
# But the library is pretty generic and you can use in-memory db for testing
# However, in case I'd have to use some NoSQL db, I'd implement a new User class with other ORM
class StatusSQLService(StatusService):
    def increment_endpoint(self, endpoint_path: str, exec_time) -> None:
        with db:
            endpoint = models.Status.get_or_none(models.Status.endpoint == endpoint_path)
            if not endpoint:
                endpoint = models.Status(endpoint=endpoint_path)
                endpoint.save(force_insert=True)
            endpoint.counter += 1
            endpoint.avg_time += exec_time / endpoint.counter
            endpoint.save()

    def get_endpoints_status(self) -> dto.RequestsStatus:
        avg_time = 0
        eps = []
        with db:
            for e in models.Status.select(models.Status).execute():
                avg_time += e.avg_time
                eps.append(dto.EndpointStatus(endpoint=e.endpoint, counter=e.counter, avg_time=e.avg_time))

        return dto.RequestsStatus(endpoints=eps, avg_time=avg_time / len(eps))
