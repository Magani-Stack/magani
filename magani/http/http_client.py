from enum import Enum
from urllib import request as client
from urllib.error import HTTPError

from magani.auth.auth import Auth

CONTENT_TYPE_VALUE = "application/json"

HTTP_OK = 200


class Response:

    def __init__(self, response):
        self.status_code = response.status
        self.status = "Success" if self.status_code == 200 else "Failed"
        self.body = response.read()

    def __str__(self):
        return str(self.__dict__)


class ErrorResponse:

    def __init__(self, **kwargs):
        self.status = "Failed"
        self.status_code = kwargs["status_code"]
        self.body = kwargs["body"]


class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class HttpErrorHandler:

    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        try:
            print("self.function :", self.function)
            if type(self.function) == type:
                return Response(self.function(*args, **kwargs))
            else:
                return Response(self.function(self, *args, **kwargs))
        except HTTPError as e:
            print("HTTPError:", e)
            response = Response(e)
            return response
        except Exception as e:
            print("Exception:", e)
            r = {
                "body": str(e),
                "status_code": 500
            }
            return ErrorResponse(**r)


def http_error_handler(function):
    def handler(*args, **kwargs):
        try:
            print("self.function :", function)
            return Response(function(*args, **kwargs))
        except HTTPError as e:
            print("HTTPError:", e)
            response = Response(e)
            return response
        except Exception as e:
            print("Exception:", e)
            r = {
                "body": str(e),
                "status_code": 500
            }
            return ErrorResponse(**r)

    return handler


class HttpClient:

    def __init__(self, api, auth_type=""):
        self.base_url = api
        self.request = client.Request(self.base_url)
        self.request.headers = Auth(auth_type).header

    def method(self, _key):
        data = {
            "GET": self.get,
            "POST": self.post,
            "PUT": self.put,
            "DELETE": self.delete
        }
        return data.get(_key)

    @http_error_handler
    def get(self, data):
        if not data:
            self.request.full_url = self.base_url
            self.request.method = Method.GET.value
            return client.urlopen(self.request)

    @http_error_handler
    def post(self, data):
        self.request.full_url = self.base_url
        self.request.method = Method.POST.value
        self.request.body = bytes(data, encoding="utf-8")
        return client.urlopen(self.request)

    @http_error_handler
    def put(self, data):
        self.request.full_url = self.base_url
        self.request.method = Method.PUT.value
        self.request.body = bytes(data, encoding="utf-8")
        return client.urlopen(self.request)

    @http_error_handler
    def delete(self, data):
        self.request.full_url = self.base_url
        self.request.method = Method.DELETE.value
        self.request.body = bytes(data, encoding="utf-8")
        return client.urlopen(self.request)


if __name__ == "__main__":
    print(HttpClient("https://www.google.com").get())
