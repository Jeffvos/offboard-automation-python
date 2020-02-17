""" Main - still work in progress """
import json
import gitlabservice
import jiraservice

with open('appconfig.json') as f:
    APPCONFIG = json.load(f)


def disable_users():
    for env in APPCONFIG['jira']['jqlurl']:
        jiraservice.Jira(env).call()


disable_users()
