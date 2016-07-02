'''
Created on 30 Jun 2016

@author: martin
'''
import unittest
import os
from coveralls_hg import api
import coverage

def make_coverage_data():
    "make coverage data"
    old = os.path.abspath(os.getcwd())
    nwd = os.path.dirname(os.path.abspath(__file__))
    os.chdir(nwd)
    cov = coverage.coverage(data_file=os.path.join(nwd, 'coverage.dat'))
    cov.start()
    coveralls = api.API('x', 'y', 'z')
    try:
        coveralls.upload_coverage()
    except: # pylint: disable=bare-except
        # we just want some coverage data, it does not really matter what it is.
        pass
    cov.stop()
    cov.save()
    os.chdir(old)


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
    @classmethod
    def setUpClass(cls):
        super(Test, cls).setUpClass()
        make_coverage_data()

    @classmethod
    def tearDownClass(cls):
        super(Test, cls).tearDownClass()
        path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(path, 'coverage.dat')
        os.remove(path)

    def setUp(self):
        api.requests = RequestsMock()
        path = os.path.dirname(os.path.abspath(__file__))
        self.path = os.path.join(path, 'coverage.dat')

    def test_01_smoke(self):
        "Just a smoke test."
        api.requests.status_code = 200
        user, repo = ENV['CI_REPO_NAME'].split('/')
        cov = api.API(user,repo, token=ENV['COVERALLS_REPO_TOKEN'])
        cov.set_source_files(self.path, strip_path='')
        cov.set_build_values()
        cov.set_dvcs_user(ENV['CI_COMMITTER_NAME'], ENV['CI_COMMITTER_EMAIL'])
        cov.set_dvcs_commit(ENV['CI_COMMIT_ID'],
                            ENV['CI_MESSAGE'],
                            ENV['CI_BRANCH'],)
        cov.upload_coverage()
        api.requests.status_code = 404
        self.assertRaises(ValueError, cov.upload_coverage)



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
    