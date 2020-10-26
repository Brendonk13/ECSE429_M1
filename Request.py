import socket
import requests
from request_types import Post, Get, Delete

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


class ThingifierServiceInactive(Exception):
    """
        Only ever raised if port_is_open() function returns false (in ImmutableRequest.__init__)
    """
    pass


class RequestStates:
    def __init__(self, url, ID, params):
        self.url = url
        self.ID = ID
        self.params = params
        self.have_changed_state = False
        self.deleted_data = False
        # store request objects like Post, Get after they have completed so we can access their state
        self.completed_requests = dict()


    def get_requests(self):
        # the requests made, in order
        return [
                Post(self.url, self.params),
                Get(self.url, ID=self.ID),
                Delete(self.url, self.ID)
        ]


    def have_done_post(self):
        return 'POST' in self.completed_requests


    def make_requests(self):
        for request in self.get_requests():
            if self.have_done_post():
                # change id to one created by the post so we delete the one just created
                new_id = self.completed_requests['POST'].created_ID
                request.set_new_id(new_id)

            request.make_request()
            print(request)
            print()
            self.verify_results(request)
            self.completed_requests.setdefault(request.name, request)


    def verify_results(self, request):
        if not request.ok:
            print(f'Exception encountered during: {request}')
            raise Exception
        if request.name == 'POST':
            # have changed the state of the application after a post
            self.have_changed_state = True
        if request.name == 'DELETE':
            # used in ImmutableRequest class to check if we did a post but never deleted the new posted data
            # if we posted but never deleted, then ImmutableRequest deletes what should have been deleted
            self.deleted_data = True


    def manually_delete_data(self):
        """ Called by immutable request instance when an error occurs """
        req = requests.delete(self.url)
        print(f'manually deleted, status_code: {req.status_code}')



class StateRestoringRequest:
    """
        restores state by making requests in the following order while also providing a context manager which handles cleanup and unexpected errors
        POST to add data
        GET to verify data was added
        DELETE to restore state
    """

    def __init__(self, url, ID=-1, json=True, params=None):
        """ Default is a get request with no parameters which returns json data """
        self.recieved_bad_input = False
        if not port_is_open():
            raise ThingifierServiceInactive
        # if ID == -1:
        #     print("don't use StateRestoringRequest without passing in a valid ID")
        #     self.recieved_bad_input = True
        #     return
        self.url = url
        self.ID = ID
        self.params = params
        self.request_states = RequestStates(self.url, self.ID, self.params)


    def __enter__(self):
        return self


    def __exit__(self, *args):
        if self.recieved_bad_input:
            return
        # print(self.recieved_bad_input)
        # print('------------------')
        if self.need_to_clean_up():
            self.request_states.manually_delete_data()


    def perform_requests(self):
        if self.recieved_bad_input:
            return
        self.request_states.make_requests()


    def need_to_clean_up(self):
        return (
            self.request_states.have_changed_state
            and not
            self.request_states.deleted_data
    )




def port_is_open():
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = ("127.0.0.1", 4567)
    return a_socket.connect_ex(location) == 0


if __name__ == "__main__":
    r = StateRestoringRequest(
        "http://localhost:4567/todos",
        ID=3,
        params={"title": "new title!"}
    )
    with r as request:
        request.perform_requests()
        print(f'------ done requests for url: {request.url} -------')


"""
next:
    create a python file with all the endpoints
    loop over endpoints and test immutableRequest
"""
