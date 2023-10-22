from base64 import b64encode
from secrets import token_bytes


def get_secret_key():
    return b64encode(token_bytes(32)).decode()


res = get_secret_key()
print(res)