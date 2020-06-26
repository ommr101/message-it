import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class Message:
    sender_id: str
    receiver_id: str
    content: str
    subject: str


@dataclass_json
@dataclass
class ReceivedMessage(Message):
    is_read: bool
    creation_date: datetime = field(metadata=config(encoder=str))


@dataclass_json
@dataclass
class User:
    username: str
    password: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass_json
@dataclass
class GetAllMessagesFilters:
    is_read: bool = field(default=None, metadata=config(decoder=lambda x: x.lower() == 'true'))


@dataclass_json
@dataclass
class EndpointStatus:
    endpoint: str
    counter: int
    avg_time: float


@dataclass_json
@dataclass
class RequestsStatus:
    endpoints: List[EndpointStatus]
    avg_time: float
