# SET UP
# terminal: pip install nose requests
# run runTodoManagerRestAPI-1.5.5.jar on localhost:4567


# to run all tests:
# terminal: nosetests --verbosity=2 tests    

from nose.tools import assert_true
import requests

apiURL = 'http://localhost:4567/todos'

def test_request_response():
    # Send a request to the API server and store the response.
    response = requests.get('http://jsonplaceholder.typicode.com/todos')

    # Confirm that the request-response cycle completed successfully.
    assert_true(response.ok)