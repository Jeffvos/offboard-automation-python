""" Gitlab service module """
import json
import requests
import jiraservice

with open('appconfig.json') as f:
    APPCONFIG = json.load(f)

GIT_BASE_URL = APPCONFIG['gitlab']['base_url']
GIT_HEADER = {"Private-Token": APPCONFIG['gitlab']['token']}

def block_user(users_to_block, jira_issue):
    """ Function to check the user and block user with second request """
    error_list = []
    for user in users_to_block[0]:
        git_user_url = GIT_BASE_URL+"users?username={}".format(user)
        user_req = requests.get(git_user_url, headers=GIT_HEADER)
        user_data = user_req.json()
        try:
            if user_data == '[]':
                error_list.append(user)
            else:
                user_id = user_data[0]['id']
                git_block_url = GIT_BASE_URL+"users/{}/block".format(user_id)
                block_req = requests.post(git_block_url, headers=GIT_HEADER)
                print(block_req)
        except IndexError:
            print('error')
            error_list.append(user)
    if error_list != []:
        print(error_list)
    else:
        jiraservice.updateticket(jira_issue)
    return True
