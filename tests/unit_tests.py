# SET UP
# terminal: pip install nose requests
# run runTodoManagerRestAPI-1.5.5.jar on localhost:4567

# to run all tests:
# terminal: nosetests --verbosity=2 tests    

from nose.tools import assert_true, assert_is_not_none, assert_list_equal
import requests

apiURL = 'http://localhost:4567/'

def test_API():
    # Send a request to the API server and store the response.
    response = requests.get(apiURL)

    # Confirm that the request-response cycle completed successfully.
    assert_true(response.ok)
    return


# for each endpoint: GET, POST, DELETE

# -------------- /todos -----------------------

def get_all_todos():
    endpoint = 'todos'
    response = requests.get(apiURL + endpoint)

    # Confirm that the request-response cycle completed successfully.
    assert_true(response.ok)
    #assert default todos have associated fields

    #delete?
    return

def get_todo_by_id():
    endpoint = 'todos'
    test_todo = [{
        'title': 'Test Todo',
        'description': 'Creating a new todo with random ID'
    }]
    
    response = requests.post(apiURL + endpoint, test_todo)

    assert(response.ok)
    assert_list_equal(test_todo, response)

    return

def post_todo():
    #post request with new title, description
    # assert that it is posted at /todos and at /todo/id
    return

def delete_todo_by_id():
    return

def post_invalid_todo():
    return

def get_todo_categories():
    return

def post_todo_link_category():
    return

def delete_todo_link_category():
    return

def get_todo_projects():
    endpoint= 'todos/id/tasksof'
    return

def post_todo_link_project():
    endpoint = 'todos/id/tasksof'
    return

def delete_todo_link_project():
    return



# -------------- /projects --------------------
def get_all_projects():
    return

def get_project_by_id():
    return

def post_project():
    return

def post_invalid_project():
    return

def delete_project_by_id():
    return

def delete_project_with_tasks():
    #deleting a project that has tasks should not delete the task
    return

def get_project_todos():
    #get the tasks associated to a project
    return

def get_project_categories():
    endpoint = '/projects/:id/categories'
    return

def post_project_link_category():
    #create a link between a project and a category (that exists or doesnt exist)
    return


# -------------- /categories ------------------
def get_all_categories():
    return

def get_category_by_id():
    return

def post_category():
    return

def delete_category_by_id():
    return

def get_category_projects():
    return

def post_category_project():
    return

def delete_category_project():
    return

def get_category_todos():
    endpoint = 'categories/id/todos/id'
    return

def post_category_todos():
    return

def delete_category_todos():
    return

# -------------- /docs----------------------
def test_docs():
    endpoint = 'docs'
    return

# ------------ /shutdown --------------------
def test_shutdown():
    return