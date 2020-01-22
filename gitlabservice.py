import requests
import time
import json
from requests.auth import HTTPBasicAuth
import jiraservice

with open('appconfig.json') as f:
    appconfig=json.load(f)

gitbaseUrl = appconfig['gitlab']['base_url']
githeaders={"Private-Token": appconfig['gitlab']['token']}

def block_user(usersToBlock, jiraIssue):
    errorList=[]
    for user in usersToBlock[0]:
        userUrl = gitbaseUrl+"users?username={}".format(user)
        userRequest = requests.get(userUrl, headers=githeaders)
        userData = userRequest.json()
        print(userData)
        try:
            if (userData=='[]'):
                errorList.append(user)
            else:
                print('Found: '+ user)
                userID=userData[0]['id']
                blockUrl= gitbaseUrl+"users/{}/block".format(userID)
                blockRequest = requests.post(blockUrl, headers=githeaders)
                print(blockRequest)
        except:
            print('error')
            errorList.append(user)
    if errorList != []:
        print(errorList)
    else:
        jiraservice.updateticket(jiraIssue)
    return
