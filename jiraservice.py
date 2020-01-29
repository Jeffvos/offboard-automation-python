"""Jira Service Module"""
import sys
import json
import requests

with open('appconfig.json') as f:
    APPCONFIG = json.load(f)

JIRA_BASE_URL = APPCONFIG['jira']['base_url']
JIRA_HEADERS = {"content-type": "application/json"}
JIRA_USER = APPCONFIG['jira']['basic_auth']['username']
JIRA_PASS = APPCONFIG['jira']['basic_auth']['password']
JIRA_AUTH = (JIRA_USER, JIRA_PASS)

def check_issues():
    """ Function to check if there is a issue in jira based on jql """
    users_to_block = []
    jira_url = JIRA_BASE_URL+APPCONFIG['jira']['jqlurl']['git-ext']
    jira_request = requests.get(jira_url, auth=JIRA_AUTH, headers=JIRA_HEADERS)
    json_res = jira_request.json()
    #for now expecting one issue if none exit
    try:
        jira_issue = json_res['issues'][0]['key']
    except IndexError:
        print('No new issues found.')
        sys.exit()
    content = json_res['issues'][0]['fields']['description']
    contentsplit = content.split()
    for items in contentsplit:
        outputm = items.find('@')
        if outputm != -1:
            users_to_block.append(items[:outputm])
    print(users_to_block)
    return users_to_block, jira_issue

def block_user(users_to_block):
    """ Function to change the users status to false """
    jira_data = "{\"active\": \"false\"}"
    suc_count = 0
    fail_count = 0
    error_list = []
    for user in users_to_block[0]:
        jira_block = JIRA_BASE_URL+"user?username={}".format(user)
        jira_req = requests.put(jira_block, data=jira_data, auth=JIRA_AUTH, headers=JIRA_HEADERS)
        jira_json = jira_req.json()
        try:
            if jira_json['errors'] != {}:
                print(jira_json['errors'])
                error_list.append(user)
                fail_count = fail_count + 1
        except IndexError:
            print('Deactivated: '+ user)
            suc_count = suc_count + 1

    print('Users deactivated: {}. Failed deactivation {}.'.format(suc_count, fail_count))

    if fail_count >= 1:
        print('Failed to deactivate users: ')
        print(error_list)
    else:
        updateticket(users_to_block[1])
    return True

def updateticket(jira_issue):
    """ Function to update jira ticket for transistion id please use the workflows close ID"""
    print("updating ticket "+ jira_issue)
    #comment = appconfig['jira']['comment']
    comment = """{
                "update":{
                    "comment":[{"add": {"body": "All Users are deactivated."}}]
                },
                "transition":{
                    "id": "171"
                    }
                }
            """
    deco = json.loads(comment)
    newcom = json.dumps(deco)
    jira_comment = JIRA_BASE_URL+"issue/"+jira_issue+"/transitions"
    c_request = requests.post(jira_comment, data=newcom, auth=JIRA_AUTH, headers=JIRA_HEADERS)
    return c_request
