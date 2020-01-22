import requests
import time
import json
from requests.auth import HTTPBasicAuth

with open('appconfig.json') as f:
    appconfig=json.load(f)

jirabaseUrl = appconfig['jira']['base_url']
jiraheaders = {"content-type": "application/json"}
jiraAuth=(appconfig['jira']['basic_auth']['username'],appconfig['jira']['basic_auth']['password'])

def check_issues():
    usersToBlock=[]
    #check for open jira offboarding issues based on JQL
    jiraUrl = jirabaseUrl+appconfig['jira']['jqlurl']['git-ext']
    jiraRequest= requests.get(jiraUrl, auth=jiraAuth, headers=jiraheaders)
    jsonRes=jiraRequest.json()
    #for now expecting one issue if none exit script
    try:
        print(len(jsonRes['issues']))
        jiraIssue=jsonRes['issues'][0]['key']
    except:
        print('No new issues found.')
        exit()
    content = jsonRes['issues'][0]['fields']['description']
    contentsplit =content.split()
    #still need to add multiple check to add to usersToBlock list
    for items in contentsplit:
        outputm=items.find('@')
        if(outputm == -1):
            continue
        else:
            usersToBlock.append(items[:outputm])
    print(usersToBlock)
    return usersToBlock, jiraIssue

def block_user(usersToBlock):
    jiraData="{\"active\": \"false\"}"
    succount=0
    failcount=0
    errorList=[]
    for user in usersToBlock[0]:
        jiraBlock = baseUrl+"user?username={}".format(user)
        jiraRequest= requests.put(jiraBlock, data=jiraData, auth=jiraAuth, headers=jiraheaders)
        jsonRes=jiraRequest.json()
        #check if transaction was successful
        try:
            if(jsonRes['errors'] != {}):
                print(jsonRes['errors'])
                errorList.append(user)
                failcount = failcount + 1
        except:
            print('Deactivated: '+ user)
            succount = succount + 1

    print('Users deactivated: {}. Failed deactivation {}.'.format(succount, failcount))

    if failcount >= 1:
        print('Failed to deactivate users: ')
        print(errorList)
    else:
        updateticket(usersToBlock[1])
    return

def updateticket(jirakey):
    print("updating ticket "+ jirakey)
    comment = appconfig['jira']['comment']
    jiraCommentUrl= jirabaseUrl+"issue/"+jirakey+"/transitions"
    commentRequest = requests.post(jiraCommentUrl, data=comment, auth=jiraAuth, headers=jiraheaders)
    return
