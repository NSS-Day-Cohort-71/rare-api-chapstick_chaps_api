import json
from http.server import HTTPServer
from request_handler import HandleRequests, status
from views import create_user, login_user
from views import get_categories, create_category
from views import get_tags, create_tag
from views import create_post, get_posts,get_postById


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

        elif url["requested_resource"] == "login":
            response = login_user(request_body)
            if response:
                return self.response(response, status.HTTP_200_SUCCESS.value)
            else:
                return self.response("", status.HTTP_500_SERVER_ERROR.value)
        elif url["requested_resource"] == "posts":
            response = create_post(request_body)
            if response:
                return self.response(response, status.HTTP_201_SUCCESS_CREATED.value)
            else:
                return self.response("", status.HTTP_500_SERVER_ERROR.value)
        elif url["requested_resource"] == "tags":
            response = create_tag(request_body)
            if response:
                return self.response(response, status.HTTP_201_SUCCESS_CREATED.value)
            else:
                return self.response("", status.HTTP_500_SERVER_ERROR.value)
        elif url["requested_resource"] == "categories":
            response = create_category(request_body)
            if response:
                return self.response(response, status.HTTP_201_SUCCESS_CREATED.value)
            else:
                return self.response("", status.HTTP_500_SERVER_ERROR.value)

    def do_GET(self):
        """Handle GET requests from a client"""

        url = self.parse_url(self.path)

        if url["requested_resource"] == "categories":
            if url["pk"] != 0:
                pass
            else:
                response = get_categories()
                if response:
                    return self.response(response, status.HTTP_200_SUCCESS.value)
                else:
                    return self.response(
                        "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                    )
        elif url["requested_resource"] == "tags":
            if url["pk"] != 0:
                pass
            else:
                response = get_tags()
                if response:
                    return self.response(response, status.HTTP_200_SUCCESS.value)
                else:
                    return self.response(
                        "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                    )
        elif url["requested_resource"] == "categories":
            if url["pk"] != 0:
                pass
            else:
                response = get_categories()
                if response:
                    return self.response(response, status.HTTP_200_SUCCESS.value)
                else:
                    return self.response(
                        "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
                    )
        elif url["requested_resource"] == "posts":
            if url["pk"] !=0:
                response_body = get_postById(url["pk"])
                if response_body:
                    return self.response(response_body, status.HTTP_200_SUCCESS.value)
                else: 
                    return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)
            
            else:
                response = get_posts()
                if response:
                    return self.response(response, status.HTTP_200_SUCCESS.value)
                else:
                    return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value)


def main():
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
