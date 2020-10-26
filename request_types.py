import json
from requests import get, post, delete

class Post:
    def __init__(self, url, params):
        self.name = 'POST'
        self.status_code = -1
        self.request = None
        self.args = [url]
        self.kwargs = {'data': json.dumps(params)}
        self.created_ID = -1
        self.response = None
        self.ok = False


    def make_request(self):
        self.request = post(*self.args, **self.kwargs)
        self.status_code, self.ok = self.request.status_code, self.request.ok
        self.response = self.request.json()
        # data = json.loads(self.response)
        if 'id' not in self.response:
            print(f'no id found in post response: {self.response}')
        else:
            self.created_ID = self.response['id']
            print(f' new id: {self.created_ID}')


    def __repr__(self):
        return f'POST:\n\trequests.post({self.args[0], self.kwargs})\n\tjson response: {self.response}\n\thttp status code: {self.status_code}'



class Get:
    def __init__(self, url, ID=None):
        self.name = 'GET'
        self.status_code = -1
        self.request = None
        self.url = url
        self.args = [url] if not ID else [url + '/' + str(ID)]
        self.response = None
        self.ok = False


    def set_new_id(self, ID):
        self.args = [self.url + '/' + str(ID)]


    def make_request(self):
        self.request = get(*self.args)
        self.status_code, self.ok = self.request.status_code, self.request.ok
        self.response = self.request.json()


    def __repr__(self):
        return f'GET:\n\trequests.get({self.args[0]})\n\tjson response: {self.response}\n\thttp status code: {self.status_code}'



class Delete:
    def __init__(self, url, ID):
        self.name = 'DELETE'
        self.status_code = -1
        self.request = None
        self.url = url
        self.args = [url + '/' + str(ID)]
        self.ok = False


    def set_new_id(self, ID):
        self.args = [self.url + '/' + str(ID)]


    def make_request(self):
        self.request = delete(*self.args)
        self.status_code, self.ok = self.request.status_code, self.request.ok


    def __repr__(self):
        return f'DELETE:\n\trequests.delete({self.args[0]})\n\thttp status code: {self.status_code}'


