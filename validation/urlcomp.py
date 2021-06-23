''' compose url for diffrent requests '''
import json
from config import config as APPCONFIG

APPCONFIG = APPCONFIG()

class Compose:
    def __init__(self):
        self._base_url = APPCONFIG['jira']['base_url']
        self._jql_url = APPCONFIG['jira']['jqlurl']
        
    def compose_url(self, method, env):
        """ composing of the url for the env"""
        options = {
                "check_issue": self._jql_url[env],
                "comment_issue": "issue/{}/transitions",
                "deactivate_user": "user?username={}"
        }
        return self._base_url + options[method]