"""
Use the codeship environmental variables to fill in the right values to upload
to coveralls.
"""

import os
from coveralls_hg.api import API

def main():
    "main script"
    user, repo = os.environ['CI_REPO_NAME'].split('/')
    api = API(user,repo,     token=os.environ['COVERALLS_REPO_TOKEN'])

    api.set_build_values(build_url=os.environ['CI_BUILD_URL'],
                            branch=os.environ['CI_BRANCH'],
                      pull_request=os.environ['CI_PULL_REQUEST'])

    api.set_dvcs_commit( commit_id=os.environ['CI_COMMIT_ID'],
                           message=os.environ['CI_MESSAGE'],
                            branch=os.environ['CI_BRANCH'])

    api.set_dvcs_user( name_author=os.environ['CI_COMMITTER_NAME'],
                      email_author=os.environ['CI_COMMITTER_EMAIL'])

    api.set_service_values( number=os.environ['CI_BUILD_NUMBER'])
    api.set_source_files('../.coverage', strip_path=os.environ['PWD'])
    api.upload_coverage()


if __name__ == '__main__':
    main()
