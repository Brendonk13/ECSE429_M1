import re
import socket

ID_PATTERN = re.compile(r'.*/(\d+)')
URL_PATTERN = re.compile(r'(.*)/\d+')
OBJECT_NAME_PATTERN = re.compile(r'.*/([a-zA-Z]+).*')

# These endpoints don't allow us to get a specific ID, more explained
# in get_request_url definition as well as where this function is called in helpers.py/Get object
NO_GET_ENDPOINTS = [
        re.compile(r'(.*/categories/\d+/todos)/(\d+)'),
        re.compile(r'(.*/categories/\d+/projects)/(\d+)'),
    ]


class ThingifierServiceInactive(Exception):
    """
        Only ever raised if port_is_open() function returns false (in ImmutableRequest.__init__)
    """
    pass


def has_id(endpoint):
    return endpoint[-1].isdecimal()


def extract_id(endpoint):
    ID = re.search(ID_PATTERN, endpoint)
    return ID.group(1) if ID else None


def url_without_id(endpoint):
    """
        input: "http://localhost:4567/todos/1234"
        output: "http://localhost:4567/todos"
    """
    if not has_id(endpoint):
        return endpoint
    url = re.search(URL_PATTERN, endpoint)
    return url.group(1)


def extract_response_id(response, object_name):
    """ return all response[object_name]['id'] in response """
    return [
        category['id']
        for category in
        response[object_name]
        if 'id' in category
    ]


def extract_object_name(endpoint):
    # note this does NOT work for /todos/id/tasksof (it would return 'tasksof') 
    # desired output: 'projects'
    return re.search(OBJECT_NAME_PATTERN, endpoint).group(1)


def get_request_url(endpoint):
    # if this endpoint does not support get request's to specific object ID's
    # then return the input url without the ID (and just get all objects instead of 1)
    for pattern in NO_GET_ENDPOINTS:
        search_result = re.search(pattern, endpoint)
        if search_result:
            return [search_result.group(1)]

    return [endpoint]


def verify_service_is_running():
    if not port_is_open():
        raise ThingifierServiceInactive


def port_is_open():
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = ("127.0.0.1", 4567)
    return a_socket.connect_ex(location) == 0

