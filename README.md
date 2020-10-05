<h1 align='center'>Python off-boarding script for Jira & Gitlab</h1>
Main functionality is to close Jira & Gitlab accounts based on a Jira ticket (JQL).

<h2>Jira</h2>

<h3>Checking for Jira tickets</h3>
First the script check if there is a ticket awaiting, based on a given JQL.
The script parses all usernames from the given ticket and checks if the account exists and if the user can be deactivated.

<h3>Closing accounts</h3>

*Jira Users will be deactivated in the Jira Directory (Not Removed)

*Gitlab user will be blocked

<h3>Jira ticket commenting and transitions</h3>
Based on the account closing result the original Jira ticket will be commented and the transition will be changed.

If there was failure/error, a comment will be added to the Jira ticket and the transition will change to Blocked.

