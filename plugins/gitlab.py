""" Gitlab service module """
import json
import requests
from clients import jira
from config import config as APPCONFIG

APPCONFIG = APPCONFIG()

class Gitlab:
    def __init__(self):
        self.instances = APPCONFIG['gitlab']
        self._base_url = APPCONFIG['gitlab']['base_url']
        self._header = {"Private-Token": APPCONFIG['gitlab']['token']}
        self._success = []
        self._failed = []

    def _compose_url(self, action):
        """ compose url based on action """
        options = {"check_user": "users?username={}",
                   "disable_user": "users/{}/block"}
        return self._base_url + options[action]

    def _success_dis(self, user):
        print(self._base_url)
        print("Deactivated user ID: ", user)

    def _request(self, method, url, user):
        """ request depending on method and url"""
        req = requests.request(method, url, headers=self._header, verify=False)
        if method == "GET":
            data_json = req.json()
            user_id = data_json[0]['id']
            return self._disable_user(user_id)
        else:
            return self._success_dis(user)

    def check_user(self, user):
        url = self._compose_url("check_user").format(user)
        return self._request("GET", url, user)

    def _disable_user(self, user_id):
        url = self._compose_url("disable_user").format(user_id)
        return self._request("POST", url, user_id)

    def check_instances(self, user):
        for git in self.instances:
            try:
                self._base_url = APPCONFIG['gitlab']['base_url']
                self._header = {
                    "Private-Token": APPCONFIG['gitlab']['token']}
                url = self._compose_url("check_user").format(user)
                self._request("GET", url, user)
            except IndexError:
                print('users not found')
