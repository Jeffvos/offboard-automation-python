""" Main - still work in progress """
import gitlabservice
import jiraservice

#example

jiraservice.block_user(jiraservice.check_issues())
gitlabservice.block_user(jiraservice.check_issues())
