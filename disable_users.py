""" Main - still work in progress """
import json
import validation
from config import config

def disable_users():
    for env in config()['jira']['jqlurl']:
        validation.Validate(env).now()

if __name__ =="__main__":
    disable_users()