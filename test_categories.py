from random import random, randrange, choice
import re
from nose.tools import assert_true, assert_equal, assert_is_not_none, assert_list_equal, assert_in
from Request import StateRestoringRequest
from request_types import Get



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
        {"title": "this is so random!", "description": "A random cool thing!"},
        {"title": "The title", "description": "good stuff here"},
        {"title": "good title", "description": "a good description"},
    ]


def category_endpoints():
    return [
        'categories/{}/todos'.format(choice(get_existing_category_IDs())),
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


def extract_response_id(response, key):
    return [
        category['id']
        for category in
        response[key]
        if 'id' in category
    ]


def get_existing_category_IDs():
    url = "http://localhost:4567/categories"
    request = Get(url)
    request.make_request()
    response = request.response
    if not response:
        return [-1]
    return extract_response_id(response, 'categories')


def test_get_categories():
    # in actual test we can assert len == 2 (initial state of application has 2 categories: 1, 2
    print(get_existing_category_IDs())


def verify_get_category_todos(request):
    """
        Called when we create a StateRestoringRequest with url of the following form:
        http://localhost:4567/categories/1/todos

        For example, if created_ID = 10
        Then the get request we would LIKE to make is: GET http://localhost:4567/categories/1/todos/10

        But the service we are testing doesn't allow this type of request
        Workaround to verify our POST with created_ID = 10 worked:
            instead do GET http://localhost:4567/categories/1/todos
            and store response for all todo's

            This function parses this response and checks if an object with id == created_ID exists
    """
    get_request = request.get_request_by_name('GET')
    response = get_request.response
    created_ID = request.get_created_ID()

    assert_in(created_ID, extract_response_id(response, 'todos'))




def test_create_delete_categories():
    for inp in get_request_inputs():
        print(inp)
        (url, ID, params) = inp
        with StateRestoringRequest(url, ID=ID, params=params) as request:
            request.perform_requests()
            if re.search(r'(.*/categories/\d+/todos)', url):
                verify_get_category_todos(request)
            print('done requests')


if __name__ == "__main__":
    # test_get_categories()
    test_create_delete_categories()
