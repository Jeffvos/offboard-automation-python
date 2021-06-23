"""Jira Service Module"""
import sys
import json
import requests
from validation.urlcomp import Compose
from config import config as APPCONFIG

Compose = Compose().compose_url

class Jira:
    """ handle jira requests """

    def __init__(self, env):
        if env not in APPCONFIG()['jira']['jqlurl']:
            print('invalid environment, check your input ')
            sys.exit()
        jira = APPCONFIG()['jira']
        self._env = env
        self._base_url = jira['base_url']
        self._headers = {"content-type": "application/json"}
        self._user = jira['basic_auth']['username']
        self._pass = jira['basic_auth']['password']
        self._auth = (self._user, self._pass)
        self._success = []
        self._failed = []


    def _put_request(self, url, user):
        """ put requests """
        jira_data = "{\"active\": \"false\"}"
        req = requests.put(url, data=jira_data, auth=self._auth,
                           headers=self._headers)
        return self._check_success(req, user)

    def _check_success(self, response, user):
        full_response = response.json()
        if response.status_code != 200:
            full_response['name'] = user
            self._failed.append(full_response)
        else:
            print("Deactivated: ", full_response['name'])
        return response

    def disable_access(self, user):
        """ deactivate in jira """
        return self._put_request(Compose(method="deactivate_user", env=self._env).format(user), user)


    def _check_transactions(self):
        pass