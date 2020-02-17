"""Jira Service Module"""
import sys
import json
import requests
import gitlabservice

with open('appconfig.json') as f:
    APPCONFIG = json.load(f)


class Jira():
    """ class to handle jira requests """

    def __init__(self, env):
        if env not in APPCONFIG['jira']['jqlurl']:
            print('invalid environment, check your input ')
            sys.exit()
        self._env = env
        self._base_url = APPCONFIG['jira']['base_url']
        self._headers = {"content-type": "application/json"}
        self._user = APPCONFIG['jira']['basic_auth']['username']
        self._pass = APPCONFIG['jira']['basic_auth']['password']
        self._auth = (self._user, self._pass)
        self._success = []
        self._failed = []

    def _compose_url(self, action):
        """ composing of the url for the env"""
        options = {
            "check_issue": APPCONFIG['jira']['jqlurl'][self._env],
            "comment_issue": "issue/{}/transitions",
            "deactivate_user": "user?username={}"
        }
        return self._base_url + options[action]

    def _handle_response(self, response):
        """ handeling response return """
        return self._check_issues(response.json())

    def _get_request(self):
        """ request creation """
        url = self._compose_url("check_issue")
        req = requests.get(url, auth=self._auth, headers=self._headers)
        return self._handle_response(req)

    def post_comment_request(self, issue_key):
        """ post request """
        url = self._compose_url("comment_issue").format(issue_key)
        comment = self._compose_comment()
        req = requests.post(url, data=comment, auth=self._auth,
                            headers=self._headers)
        return req.status_code

    def _put_request(self, url, user):
        """ put requests """
        jira_data = "{\"active\": \"false\"}"
        req = requests.put(url, data=jira_data, auth=self._auth,
                           headers=self._headers)
        return self._check_success(req, user)

    def _check_issues(self, response):
        """ check if there are any open issues"""
        if response['total'] == 0:
            print('no new issues for env', self._env)
        return self._check_issue_count(response)

    def _convert_issue(self, issue_body, issue_key):
        """ creation of users to block list for"""
        to_disable = []
        issue = issue_body.split()
        for item in issue:
            mail_position = item.find('@')
            if mail_position != -1:
                current_user = item[:mail_position]
                to_disable.append(current_user)
                if self._env == "jira":
                    self._disable_access(current_user)
                else:
                    gitlabservice.Gitlab().check_user(current_user)
        return self._update_issue(issue_key)

    def _check_issue_count(self, response):
        """ check the amount of issues """
        if response['total'] == 1:
            return self._convert_issue(
                response['issues'][0]['fields']['description'],
                response['issues'][0]['key'])
        return self._multiple_issues(response)

    def _multiple_issues(self, response):
        issue_number = 0
        while issue_number < response['total']:
            self._convert_issue(
                response['issues'][issue_number]['fields']['description'],
                response['issues'][issue_number]['key'])
            issue_number += 1
        return issue_number

    def _check_success(self, response, user):
        full_response = response.json()
        if response.status_code != 200:
            full_response['name'] = user
            self._failed.append(full_response)
        else:
            print("Deactivated: ", full_response['name'])
        return response

    def _disable_access(self, to_disable):
        """ deactivate in jira """
        return self._put_request(self._compose_url(
            "deactivate_user").format(to_disable), to_disable)

    def _compose_comment(self):
        """ composing the comment """
        issue_comment = APPCONFIG['jira']['comment']
        return json.dumps(issue_comment)

    def _check_transactions(self):
        pass

    def _update_issue(self, issue_key):
        """ update the jira issue and close the it """
        if len(self._failed) == 0:
            return self.post_comment_request(issue_key)
        print("Double check: ", self._failed)
        return self._failed

    def call(self):
        """ init call """
        return self._get_request()
