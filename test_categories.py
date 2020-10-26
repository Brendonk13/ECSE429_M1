from Request import StateRestoringRequest
from request_types import Get
from random import random, randrange, choice
import re

ID_PATTERN = re.compile(r'.*/(\d+)')




def rand_num():
    # random number from random range 1 -> random() * 1000
    return randrange(1, int(random() * 1000))


def has_id(endpoint):
    return endpoint[-1].isdecimal()


def extract_id(endpoint):
    ID = re.search(ID_PATTERN, endpoint)
    return ID.group(1) if ID else None


def random_request_parameters(number_params):
    return [
        random_request_parameter()
        for _ in range(number_params)
    ]


def random_request_parameter():
    return choice(request_parameters())


def request_parameters():
    return [
        {"title": "random new title!"},
        {"title": "random title !"},
        {"description": "A random cool thing!"},
        {"title": "The title", "description": "good stuff here"},
        {"description": "random descriptions"},
        {"title": "good title", "description": "a good description"},
    ]


def category_endpoints():
    return [
        'categories/{}/todos'.format(rand_num()),
    ]
# 'categories',
# 'categories/{}'.format(rand_num()),


def get_urls():
    base_url = "http://localhost:4567/"
    return [
        base_url + endpoint
        for endpoint in
        category_endpoints()
    ]


def get_request_inputs():
    ID = None
    inputs = []
    for url in get_urls():
        ID = -1 if not has_id(url) else extract_id(url)
        inputs.append((url, ID, random_request_parameter()))
    return inputs


def test_get_categories():
    url = "http://localhost:4567/categories"
    request = Get(url)
    request.make_request()
    response = request.response['categories']
    # response = request.response
    print(response)
    print('--------------------------')
    if response and 'id' in response:
        print(f"{response['id']}")


def test_create_delete_categories():
    for inp in get_request_inputs():
        print(inp)
        (url, ID, params) = inp
        with StateRestoringRequest(url, ID, params) as request:
            request.perform_requests()

if __name__ == "__main__":
    test_get_categories()
