''' Validation of jira request '''
import requests
import json
from validation.urlcomp import Compose
from plugins import jira, gitlab
from clients.jira import Client as jira_client
from config import config as APPCONFIG

jira_client = jira_client()

Compose = Compose()
APPCONFIG = APPCONFIG()

class Validate:
    def __init__(self, env):
        if env not in APPCONFIG['jira']['jqlurl']:
            print('invalid environment')
            sys.exit()
        self._env = env
        self.jira = jira.Jira(env)
        self._base_url = APPCONFIG['jira']['base_url']
        self._headers = {"content-type": "application/json"}
        self._user = APPCONFIG['jira']['basic_auth']['username']
        self._pass = APPCONFIG['jira']['basic_auth']['password']
        self._auth = (self._user, self._pass)
    
    def _get_request(self):
        """ request creation """
        url = Compose.compose_url(method="check_issue", env=self._env)
        req = requests.get(url, auth=self._auth, headers=self._headers)
        return self._handle_response(req)

    def _handle_response(self, response):
        """ handling response return """
        print(response)
        return self._check_issues(response.json())

    def _check_issues(self, response):
        """ check if there are any open issues"""
        if response['total'] == 0:
            print('no new issues for env', self._env)
        return self._count_issues(response)
    
    def _count_issues(self, response):
        """ check the amount of open issues """
        if response['total'] == 1:
            return self._final_validation(
                response['issues'][0]['fields']['description'],
                response['issues'][0]['key'])
        return self._multiple_issues(response)
    
    def _multiple_issues(self, response):
        issue_number = 0
        while issue_number < response['total']:
            self._final_validation(
                response['issues'][issue_number]['fields']['description'],
                response['issues'][issue_number]['key'])
            issue_number += 1
        return issue_number

    def _final_validation(self, issue_body, issue_key):
        """ creation of users to block list """
        to_disable = []
        issue = issue_body.split()
        for item in issue:
            mail_position = item.find('@')
            if mail_position != -1:
                current_user = item[:mail_position]
                to_disable.append(current_user)
                if self._env == "jira":
                    self.jira.disable_access(user=current_user)
                else:
                    gitlab.Gitlab().check_instances(current_user)
        return jira_client.update_issue(issue_key, self._env)

    def now(self):
        return self._get_request()