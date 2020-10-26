import requests
import json
# from contextlib import contextmanager
from dataclasses import dataclass

""" Notes

    POST:
        cannot end with id
        no trailing slash allowed

    GET:
        optional trailing ID
        no trailing slash allowed

    DELETE:
        MUST specify an ID
        trailing slash: allowed (no err code) but does nothing
"""

@dataclass
class RequestParent:
    url : str
    request_args: tuple
    request_kwargs: dict
    status_code: int = -1
    response: str = None


# class Post(RequestParent):
class Post:
    def __init__(self, url, params):
        self.status_code = -1
        self.request = None
        self.args = (url, )
        self.kwargs = {'data': json.dumps(params)}

    def __call__(self):
        self.request = requests.delete(*self.args, **self.kwargs)

class Get:
    def __init__(self, url, ID=None):
        self.status_code = -1
        self.request = None
        self.args = (url, )
        if ID:
            self.args += '/' + str(ID)

    def __call__(self):
        self.request = requests.delete(*self.args)

class Delete:
    def __init__(self, url, ID):
        self.args = (url + ID, )
        self.status_code = -1
        self.request = None

    def __call__(self):
        self.request = requests.delete(*self.args)


# need something that just is the correct values instead of all these cases


# new name: Request_state
class Request:
    """ does a POST to the desired endpoint """
    def __init__(self, url, params):
        self.url = url
        self.params = params
        self.request = None
        self.response = ''
        self.status_code = -1
        # incremented every time a request is made
        self.number_requests_made = 0
        self.have_changed_state = False
        self.worked = False
        self.deleted_data = False
        # self.headers = {'content-type': 'application/json'}


    def get_request_type(self):
        """ for debugging, used in __repr__ """
        if self.number_requests_made == 0:
            return 'None made yet'
        if self.number_requests_made == 1:
            return 'POST'
        if self.number_requests_made == 2:
            return 'GET'
        if self.number_requests_made == 3:
            return 'DELETE'

    def __repr__(self):
        return f'\trequest type: {self.get_request_type()} -> made to url: {self.url}\n\tparameters: {self.params}\n\thttp status code: {self.status_code}\n\tjson response: {self.response}'

    def store_response(self):
        if self.number_requests_made in (0, 1):
            self.response = self.request.json()
            print(f'response: {self.response}')

    def __call__(self, *args, **kwargs):
        # print(f'args: {args}')
        self.request = self.request_type(*args, **kwargs)
        self.store_response()
        self.status_code = self.request.status_code
        self.worked = self.request.ok

    def get_POST_args(self):
        print(f'POST: {self.url}')
        self.have_changed_state = True
        self.request_type = requests.post
        return (self.url,), {'data': json.dumps(self.params)} if self.params else (self.url, )

    def get_GET_args(self):
        print(f'GET: {self.url}')
        self.request_type = requests.get
        # return (self.url,),  {'params': self.params} if self.params else (self.url, )
        return (self.url, ), None

    def get_DELETE_args(self):
        print(f'DELETE: {self.url}')
        self.request_type = requests.delete
        self.deleted_data = True
        return (self.url, ), None

    def get_args(self):
        if self.number_requests_made == 0:
            # first request is a POST to create data
            return self.get_POST_args()
        elif self.number_requests_made == 1:
            # second request is a GET to verify that the post worked
            return self.get_GET_args()
        elif self.number_requests_made == 2:
            # third request is a DELETE to restore application state to before the first request: POST
            return self.get_DELETE_args()
        else:
            print('This should not happen, means a request was made after the DELETE')
            raise Exception

    def make_request(self):
        # doing just self(args) equivalent to self.__call__(args)
        args, kwargs = self.get_args()
        if kwargs:
            self(*args, **kwargs)
        else:
            self(*args)
        self.number_requests_made += 1

    def manually_delete_data(self):
        """ Called by immutable request instance when an error occurs """
        req = requests.delete(self.url)
        print(f'manually deleted, status_code: {req.status_code}')



class ImmutableRequest:
    """
        Immutable because the state of the application is the same after the 3 requests are made
        requests made:
        POST
        GET to verify post worked
        DELETE to restore state
    """

    def __init__(self, url, json=True, params=None):
        """ Default is a get request with no parameters which returns json data """
        self.url = url
        self.params = params
        self.request = Request(self.url, self.params)

    def make_request(self):
        # print('before request')
        self.request.make_request()
        if not self.request.worked:
            print(self.request)
            raise Exception

    def make_requests(self):
        self.make_request()
        self.make_request()
        self.make_request()

    def __enter__(self):
        return self

    def need_to_clean_up(self):
        return (
            self.request.have_changed_state
            and not
            self.request.deleted_data
    )

    def __exit__(self, *args):
        if self.need_to_clean_up():
            self.request.manually_delete_data()


if __name__ == "__main__":
    r = ImmutableRequest(
        "http://localhost:4567/todos/3",
        params={"title": "new title!"}
    )
    with r as request:
        request.make_requests()
        print(f'------ done requests for url: {request.url} -------')

