import json
from http.server import HTTPServer
from request_handler import HandleRequests, status
from views import create_user


class JSONServer(HandleRequests):

    def do_POST(self):
        """Handle POST requests from a client"""
        url = self.parse_url(self.path)

        content_len = int(self.headers.get("content-length", 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "register":
            successfully_created = create_user(request_body)
            if successfully_created:
                return self.response(
                    successfully_created, status.HTTP_201_SUCCESS_CREATED.value
                )
            else:
                return self.response(
                    "registration failed",
                    status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
                )


def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
