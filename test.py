'''
Created on 30 Jun 2016

@author: martin
'''
import unittest
import os
from coveralls_hg import api, coveralls_codeship

class RequestsMock():
    "Requests Mock"
    def __init__(self):
        self.status_code = 200
        self.data_json = None
        self.data_post = None
        self.data = dict()

    def post(self, url, files):
        "POST"
        self.data[url] = files
        return self

    def get(self, url):
        "GET"
        if not '1' in url:
            self.data_json = {'builds':[]}
        elif 'dontmindme' in url:
            self.data_json = {'rubbish':True}
        else:
            self.data_json = {'builds':['one']}
        return self

    def raise_for_status(self):
        "Raise an error"
        if self.status_code >= 200 and self.status_code < 300:
            return False
        raise ValueError('raise for status')

    def json(self):
        "Return json data."
        return self.data_json


ENV = {'CI_REPO_NAME':'hellwig/django-integrator',
       'CI_PULL_REQUEST':'false',
       'CI_MESSAGE':'moved uploading of pypi pacakge to deployment',
       'CI_COMMIT_ID':'ead7801b4f620a45b8ae7c4e73e55d19c0f1cd61',
       'CI_COMMITTER_NAME':"Martin P. Hellwig",
       'CI_COMMITTER_EMAIL':'martin.hellwig@gmail.com',
       'CI_BUILD_URL':'https://codeship.com/projects/123456/builds/1234567',
       'CI_BUILD_NUMBER':'1234567',
       'CI_BRANCH':'default',
       'COVERALLS_REPO_TOKEN':'deadbeef',
       'PWD':os.environ['PWD']}

# pylint: disable=missing-docstring, protected-access
class Test(unittest.TestCase):
    def setUp(self):
        api.requests = RequestsMock()
        path = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(path, 'test_data', 'coverage')

    def test_01_smoke(self):
        "Just a smoke test."
        api.requests.status_code = 200
        coveralls_codeship.main(ENV, self.path)

    def test_02_smoke_error(self):
        "Smoke test for error."
        api.requests.status_code = 400
        self.assertRaises(ValueError, coveralls_codeship.main, ENV, self.path)


    def test_03_get_builds_error(self):
        "Test fetching of data"
        api.requests.status_code = 404
        user, repo = ENV['CI_REPO_NAME'].split('/')
        cov = api.API(user,repo, token=ENV['COVERALLS_REPO_TOKEN'])
        self.assertRaises(ValueError, list, cov.list_builds())

    def test_04_get_builds_empty(self):
        "Test fetching of data"
        api.requests.status_code = 200
        user, repo = ENV['CI_REPO_NAME'].split('/')
        cov = api.API(user,repo, token=ENV['COVERALLS_REPO_TOKEN'])
        expected = 1
        actually = len(list(cov.list_builds()))
        self.assertEqual(expected, actually)

    def test_05_get_builds_empty(self):
        "Test fetching of data"
        api.requests.status_code = 200
        user, repo = ENV['CI_REPO_NAME'].split('/')
        cov = api.API(user,repo, token=ENV['COVERALLS_REPO_TOKEN'])
        actually = len(list(cov.builds('dontmindme')))
        expected = 1
        self.assertEqual(expected, actually)

    def test_10_set_with_remote(self):
        "Test setting data."
        user, repo = ENV['CI_REPO_NAME'].split('/')
        _ = api.API(user,repo, token=ENV['COVERALLS_REPO_TOKEN'])
        _.set_dvcs_commit('id', 'message', 'branch', ['remotes'])
        self.assertIn('remotes', _.settings['UPLOAD']['git'])

    def test_11_check(self):
        "Test setting data."
        user, repo = ENV['CI_REPO_NAME'].split('/')
        _ = api.API(user,repo, token=ENV['COVERALLS_REPO_TOKEN'])
        self.assertRaises(ValueError, _._check_upload)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_first']
    unittest.main()
