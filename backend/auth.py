from api.client import Post
import requests


class Auth:
    def __init__(self):
        self.post = Post("https://airportgap.com/api")

    def get_token(self, username, password, session=False):
        payload = {"email": username, "password": password}
        if session:
            r = self.post.post_with_json_payload("/tokens", json=payload)
            return r
        else:
            r = self.post.post_with_json_payload("/tokens", json=payload)
            return r
