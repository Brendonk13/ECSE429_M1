from random import random, randrange, choice
import re
from nose.tools import assert_true, assert_equal, assert_is_not_none, assert_list_equal, assert_in, assert_not_in
from Request import StateRestoringRequest
from request_types import Get
from helpers import has_id, extract_id, extract_response_id, extract_object_name


def original_response(endpoint):
    """
        This function returns the response that the server would make if no state changes have been made to the application
        The returned values are the result of (copy-pasted): curl -X GET -H 'Content-Type: application/json'  http://localhost:4567/$endpoint
    """
    base_url_length = len("http://localhost:4567/")
    # extract test after base url to avoid typing full url in if statements
    endpoint = endpoint[base_url_length:]

    if endpoint == 'categories':
        return {"categories":[{"id":"1","title":"Office","description":""},{"id":"2","title":"Home","description":""}]}

    if endpoint in ('categories/1/todos', 'categories/2/todos'):
        return {"todos":[]}

    if endpoint in ('categories/1/projects', 'categories/2/projects'):
        return {"projects":[]}


def rand_num():
    # random number from random range 1 -> random() * 1000
    return randrange(1, int(random() * 1000))

def random_request_parameters(number_params):
    return [
        random_request_parameter()
        for _ in range(number_params)
    ]


def random_request_parameter():
    return choice(request_parameters())


def request_parameters():
    return [
        {"title": "this is a new title!"},
        {"title": "new title !"},
        {"title": "this is so random!", "description": "A random cool thing!"},
        {"title": "The title", "description": "good stuff here"},
        {"title": "good title", "description": "a good description"},
    ]


def category_endpoints():
    existing_IDs = get_existing_category_IDs()
    return [
        'categories/{}/todos'.format(choice(existing_IDs)),
        'categories',
        'categories/{}/projects'.format(choice(existing_IDs)),
    ]


def get_tested_endpoints():
    base_url = "http://localhost:4567/"
    return [
        base_url + endpoint
        for endpoint in
        category_endpoints()
    ]


def get_request_inputs():
    """
        store a series of (url, id, parameters)
        to use as input for a StateRestoringRequest object
    """
    ID = None
    inputs = []
    for url in get_tested_endpoints():
        ID = -1 if not has_id(url) else extract_id(url)

        inputs.append((url, ID, random_request_parameter()))
    return inputs



def get_existing_category_IDs():
    url = "http://localhost:4567/categories"
    request = Get(url)
    request.make_request()
    response = request.response
    if not response:
        return [-1]
    return extract_response_id(response, 'categories')


def test_get_all():
    """
        performs get requests on each possible category endpoint
        queries ALL objects per endpoint and verifies by comparing the response to the original state of the application's equivalent response
    """
    for endpoint in get_tested_endpoints():
        request =  Get(endpoint)
        request.make_request()
        print(f'found   : {request.response}\noriginal: {original_response(endpoint)}\n')
        assert_equal(request.response, original_response(endpoint))



def test_get_categories():
    # initial state of application has 2 categories: 1, 2
    assert(len(get_existing_category_IDs()) == 2)


def verify_post_created_object(request, object_name):
    # state before post
    original_state = request.request_states.original_state
    # ID of new object created by post
    created_ID = request.get_request_by_name('POST').created_ID

    # if the created_ID isn't in the original state but is after the post, then the post was successful
    assert_not_in(created_ID, extract_response_id(original_state, object_name))


def verify_state_preserved(request):
    """
        Called after all requests made to an endpoint
        checks that the original state before any requests is the same as the current state (after requests made)
    """
    original_state = request.request_states.original_state
    assert_equal(original_state, request.request_states.get_current_state())


def verify_get_worked(request, object_name):
    """
        We check if the new ID from POST appears in the response from the GET
    """
    get_request = request.get_request_by_name('GET')
    response = get_request.response
    created_ID = request.get_created_ID()

    assert_in(created_ID, extract_response_id(response, object_name))



def verify_all_operations(request, object_name):
    # verify post worked
    verify_post_created_object(request, object_name)
    # verify that get worked
    verify_get_worked(request, object_name)
    # verify delete worked
    verify_state_preserved(request)


def test_create_delete_categories():
    for inp in get_request_inputs():
        print(inp)
        (url, ID, params) = inp
        with StateRestoringRequest(url, ID=ID, params=params) as request:
            request.perform_requests()
            verify_all_operations(request, extract_object_name(url))
            print('----------------- done requests for url: {} ---------------\n'.format(url))


if __name__ == "__main__":
    # test_get_categories()
    test_create_delete_categories()
    test_get_all()



"""
Done:
    get all /categories/
    /categories/id/todos/id - this isn't actually a bug tho ..
    /categories/:id/projects/:id
    /categories/id

next:
    Add a GET before anythign in StateRestoringRequest
    -- then show that the created_ID in POST didn't exist in the original state
    -- then GET shows the created_ID was actually stored
    -- then show that created_ID not in response after DELETE

    remove bug notice about /categories/id/todos/id
    -- We only test DELETE for this
        - but this IS undocumented behaviour!! (I was able to POST, not mentioned !!!!!!!!!!)



    /categories/:id/projects

"""
