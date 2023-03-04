import requests

from app.database import models
from config import conf

base_url = f'http://{conf.HOST}:{conf.PORT}/'

user1_details = {
    "username": "dan",
    "password": "123"
}

user1_signup_res = requests.post(base_url + 'api/v1/auth/signup', json=user1_details)
user1_details["id"] = user1_signup_res.json()["user_id"]

user1_signip_res = requests.post(base_url + 'api/v1/auth/signin', json=user1_details)
user1_details["token"] = user1_signip_res.json()["token"]

user2_details = {
    "username": "omer",
    "password": "123"
}

user2_signup_res = requests.post(base_url + 'api/v1/auth/signup', json=user2_details)
user2_details["id"] = user2_signup_res.json()["user_id"]

user2_signip_res = requests.post(base_url + 'api/v1/auth/signin', json=user2_details)
user2_details["token"] = user2_signip_res.json()["token"]

message1_details = {
    "sender_id": user1_details["id"],
    "receiver_id": user2_details["id"],
    "content": "test",
    "subject": "TEST"
}

send_message1_res = requests.post(base_url + 'api/v1/messages', json=message1_details,
                                  headers={'Authorization': f'Bearer {user1_details["token"]}'})
message1_details["id"] = send_message1_res.json()["message_id"]

message2_details = {
    "sender_id": user1_details["id"],
    "receiver_id": user2_details["id"],
    "content": "test2",
    "subject": "TEST2"
}

send_message2_res = requests.post(base_url + 'api/v1/messages', json=message2_details,
                                  headers={'Authorization': f'Bearer {user1_details["token"]}'})
message2_details["id"] = send_message2_res.json()["message_id"]

message3_details = {
    "sender_id": user2_details["id"],
    "receiver_id": user1_details["id"],
    "content": "test3",
    "subject": "TEST3"
}

send_message3_res = requests.post(base_url + 'api/v1/messages', json=message3_details,
                                  headers={'Authorization': f'Bearer {user2_details["token"]}'})
message3_details["id"] = send_message3_res.json()["message_id"]

read_message1 = requests.get(base_url + f'api/v1/messages/{message1_details["id"]}',
                             headers={'Authorization': f'Bearer {user2_details["token"]}'})
print(read_message1.json())

get_all_user2_messages = requests.get(base_url + 'api/v1/messages',
                                      headers={'Authorization': f'Bearer {user2_details["token"]}'})
print(get_all_user2_messages.json())

get_user2_read_messages = requests.get(base_url + f'api/v1/messages', params={'is_read': True},
                                       headers={'Authorization': f'Bearer {user2_details["token"]}'})
print(get_user2_read_messages.json())

get_user2_unread_messages = requests.get(base_url + 'api/v1/messages', params={'is_read': False},
                                         headers={'Authorization': f'Bearer {user2_details["token"]}'})
print(get_user2_unread_messages.json())

delete_user2_message1 = requests.delete(base_url + f'api/v1/messages/{message1_details["id"]}',
                                        headers={'Authorization': f'Bearer {user2_details["token"]}'})
get_all_user2_messages = requests.get(base_url + 'api/v1/messages',
                                      headers={'Authorization': f'Bearer {user2_details["token"]}'})
assert not get_all_user2_messages.json()

delete_user1_message1 = requests.delete(base_url + f'api/v1/messages/{message1_details["id"]}',
                                        headers={'Authorization': f'Bearer {user1_details["token"]}'})

assert not models.Sender.get_or_none(
    models.Sender.message == message1_details["id"] and models.Sender.sender == user1_details["id"])

assert not models.Message.get_or_none(models.Message.id == message1_details["id"])



# omer omer omer omer
