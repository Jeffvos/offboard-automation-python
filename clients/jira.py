''' 

jira client to update issues

'''
import requests
import json
from validation.urlcomp import Compose
from config import config as APPCONFIG

Compose = Compose().compose_url
APPCONFIG =APPCONFIG()

class Client:
    def __init__(self):
        self._headers = {"content-type": "application/json"}
        self._user = APPCONFIG['jira']['basic_auth']['username']
        self._pass = APPCONFIG['jira']['basic_auth']['password']
        self._auth = (self._user, self._pass)
        self._failed = []
        self._env = ""

    def update_issue(self, issue_key, env):
        self._env = env
        message = ""
        if len(self._failed) == 0:
            message = "Users are disabled"
            return self.post_comment_request(issue_key, message)
        else:
            message = self._failed[0]['errors']
            print(message)
            failed_user = self._failed[0]['name']
            message['active'] = message['active'] + ' user: ' + failed_user
            print("Double check: ", message['active'])
            self.post_comment_request(issue_key, {"comment": message['active']})
            self._failed = []
            return message

    def _compose_comment(self, message):
        """ composing the comment """
        APPCONFIG['jira']['comment']['update']['comment'][0]['add']['body'] = message
        issue_comment = APPCONFIG['jira']['comment']
        print(issue_comment)
        return json.dumps(issue_comment)

    def post_comment_request(self, issue_key, message):
        """ post comment request, checks if the type equals to dict and changes the transition (to blocked) """
        if isinstance(message, dict):
            APPCONFIG['jira']['comment']['transition']['id'] = "161"
            comment = self._compose_comment(message['comment'])
            print(APPCONFIG['jira']['comment']['transition']['id'])
        else:
            comment = self._compose_comment(message)
        url = Compose("comment_issue", self._env).format(issue_key)
        req = requests.post(url, data=comment, auth=self._auth,
                            headers=self._headers)
        print(req.text)
        return req.status_code
