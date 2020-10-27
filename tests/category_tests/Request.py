import socket
import requests
from request_types import Post, Get, Delete
from helpers import has_id, extract_id, extract_response_id, url_without_id, verify_service_is_running



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
        """
            the requests made, in order:
            POST endpoint
            GET  endpoint/created_ID
            DELETE endpoint/created_ID
        """
        return [
                Post(self.url, self.params),
                Get(self.url, ID=self.ID),
                Delete(self.url, self.ID)
        ]


    def have_done_post(self):
        return 'POST' in self.completed_requests


    def get_current_state(self):
        get_all_url = url_without_id(self.url) if has_id(self.url) else self.url
        # removing the id from the url means we will retrieve all objects at this endpoint
        request = Get(get_all_url)
        request.make_request()
        return request.response


    def store_initial_state(self):
        """
            We store the initial state to verify that POST worked: (check that created_ID not in the initial state)
            And also to verify that the DELETE worked: assert(initial_state = state after DELETE)
        """
        # called before changing state therefore this is the original state
        self.original_state = self.get_current_state()


    def make_requests(self):
        self.store_initial_state()
        for request in self.get_requests():
            if self.have_done_post():
                # change id to one created by the post so we delete the one just created
                new_id = self.completed_requests['POST'].created_ID
                request.set_new_id(new_id)

            request.make_request()
            self.verify_results(request)
            self.completed_requests.setdefault(request.name, request)


    def verify_results(self, request):
        if request.request and not request.request.ok:
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
        print('manually deleted, status_code: {}'.format(req.status_code))


class StateRestoringRequest:
    """
        restores state by making requests in the following order while also providing a context manager which handles cleanup and unexpected errors
        POST to add data
        GET to verify data was added
        DELETE to restore state
    """


    def __init__(self, url, ID=-1, json=True, params=None):
        """ Default is a get request with no parameters which returns json data """
        verify_service_is_running()
        self.url = url
        self.ID = ID
        self.params = params
        self.request_states = RequestStates(self.url, self.ID, self.params)


    def __enter__(self):
        return self


    def __exit__(self, *args):
        if self.need_to_clean_up():
            # print('need to cleanup')
            self.request_states.manually_delete_data()


    def get_request_by_name(self, name):
        return self.request_states.completed_requests[name]


    def get_created_ID(self):
        """
            Returns the ID of the created object when the post request was made
        """
        return self.request_states.completed_requests['POST'].created_ID


    def perform_requests(self):
        self.request_states.make_requests()


    def need_to_clean_up(self):
        return (
            self.request_states.have_changed_state
            and not
            self.request_states.deleted_data
    )




if __name__ == "__main__":
    r = StateRestoringRequest(
        "http://localhost:4567/todos",
        ID=3,
        params={"title": "new title!"}
    )
    with r as request:
        request.perform_requests()
        print('------ done requests for url: {} -------'.format(request.url))
