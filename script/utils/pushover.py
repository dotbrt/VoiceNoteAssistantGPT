import requests


class Client:
    def __init__(self, user_key, api_token, api_url="https://api.pushover.net/1/messages.json"):
        self.user_key = user_key
        self.token = api_token
        self.api_url = api_url

    def send_message(self, message, title=None, priority=None, device=None, url=None, url_title=None):
        payload = {
            "user": self.user_key,
            "token": self.token,
            "message": message,
        }

        if title:
            payload["title"] = title

        if priority:
            payload["priority"] = priority

        if device:
            payload["device"] = device

        if url:
            payload["url"] = url

        if url_title:
            payload["url_title"] = url_title
        response = requests.post(self.api_url, data=payload)
        return response.json()

    # def print_every_self(self):
    #     print("USERKEY ", self.user_key)
    #     print("TOKEN ", self.token)
    #     print("URL ", self.api_url)
