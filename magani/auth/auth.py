from base64 import b64encode

CONTENT_TYPE_VALUE = "application/json"


class AuthType:
    NoAuth = ""
    BasicAuth = "basic"


class NoAuth:

    def __init__(self):
        self.header = {
            "content-type": CONTENT_TYPE_VALUE,
        }


class BasicAuth:

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password
        auth_bytes = bytes('{}:{}'.format(user_name, password), encoding="ascii")
        basic_auth = b64encode(auth_bytes).decode("ascii")
        self.header = {
            "content-type": CONTENT_TYPE_VALUE,
            "Authorization": "Basic {}".format(basic_auth)
        }


class Auth(NoAuth, BasicAuth):

    def __init__(self, auth_type, **kwargs):
        if AuthType.BasicAuth == auth_type:
            BasicAuth.__init__(self, **kwargs)
        else:
            NoAuth.__init__(self)
            self.header = {
                "content-type": CONTENT_TYPE_VALUE,
            }


if __name__ == "__main__":
    up = {"user_name": "user", "password": "12345"}
    print(Auth(None, **up).header)
    print(Auth("basic", **up).header)
