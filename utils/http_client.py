from urllib import request as client
from urllib.error import HTTPError
from enum import Enum
import json

CONTENT_TYPE_VALUE = "application/json"

HTTP_OK = 200


class Response:

    def __init__(self, response):
        self.status_code = response.status
        self.body = response.read()

    def __str__(self):
        return str(self.__dict__)


class Method(Enum):
    GET = "GET"


class HttpClient:

    def __init__(self, api):
        self.base_url = api
        self.request = client.Request(self.base_url)
        self.request.headers = {
            "content-type": CONTENT_TYPE_VALUE,
        }

    def get(self):
        try:
            self.request.full_url = self.base_url
            self.request.method = Method.GET.value
            http_response = client.urlopen(self.request)
            response = Response(http_response)
            return response
        except HTTPError as e:
            print(e)
            response = Response(e)
            return response
        except Exception as e:
            print(e)
            r = {
                "body": str(e),
                "status_code": 500
            }
            return json.loads(json.dumps(r))


if __name__ == "__main__":
    print(HttpClient("https://www.google.com").get())
