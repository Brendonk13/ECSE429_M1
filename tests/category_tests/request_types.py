import json
from requests import get, post, delete
from re import search
from helpers import get_request_url

class Post:
    def __init__(self, url, params):
        self.name = 'POST'
        self.request = None
        self.args = [url]
        self.kwargs = {'data': json.dumps(params)}
        self.created_ID = -1
        self.response = None


    def make_request(self):
        self.request = post(*self.args, **self.kwargs)
        self.response = self.request.json()
        if 'id' not in self.response:
            print("POST request to endpoint: '{}' failed, no new object created.".format(self.args[0]))
        else:
            self.created_ID = self.response['id']
            # print(f' new id: {self.created_ID}')


    def __repr__(self):
        return 'POST:\n\trequests.post({})\n\tjson response: {}\n\thttp status code: {}'.format(
            (self.args[0], self.kwargs), self.response, self.request.status_code
        )



class Get:
    def __init__(self, url, ID=None):
        self.name = 'GET'
        self.request = None
        self.url = url
        self.args = [url] if not ID else [url + '/' + str(ID)]
        self.response = None


    def set_new_id(self, ID):
        self.args = [self.url + '/' + str(ID)]
        self.url  = self.args[0]


    def make_request(self):
        # this fxn handles endpoints which do not support get requests
        self.args = get_request_url(self.url)

        self.request = get(*self.args)
        self.response = self.request.json()


    def get_status_code(self):
        """
            need to wrap this since sometimes we don't make a request (thus self.request = None) happens (when given categories/num/todos/num endpoint)
        """
        return self.request.status_code if self.request else -1


    def __repr__(self):
        return 'GET:\n\trequests.get({})\n\tjson response: {}\n\thttp status code: {}'.format(
            self.args[0], self.response, self.get_status_code()
        )




class Delete:
    def __init__(self, url, ID):
        self.name = 'DELETE'
        self.request = None
        self.url = url
        self.args = [url + '/' + str(ID)]


    def set_new_id(self, ID):
        self.args = [self.url + '/' + str(ID)]


    def make_request(self):
        self.request = delete(*self.args)


    def __repr__(self):
        return 'DELETE:\n\trequests.delete({})\n\thttp status code: {}'.format(
            self.args[0], self.request.status_code
        )


