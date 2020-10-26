import re

ID_PATTERN = re.compile(r'.*/(\d+)')
URL_PATTERN = re.compile(r'(.*)/\d+')
OBJECT_NAME_PATTERN = re.compile(r'.*/([a-zA-Z]+).*')

def has_id(endpoint):
    return endpoint[-1].isdecimal()


def extract_id(endpoint):
    ID = re.search(ID_PATTERN, endpoint)
    return ID.group(1) if ID else None


def url_without_id(endpoint):
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


