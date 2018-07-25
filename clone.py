#!/usr/bin/env python

import argparse
import os
from github3 import login


API_PASSWORD = ''
API_USER = ''
url = 'https://api.github.com/'
orgs = [""]
gh = login('', '')

def setargs(args):
    global API_KEY
    global API_USER
    global gh
    if args.api_key != None:
        API_KEY = args.api_key
        print("Would have set var:" + API_KEY)
    if args.username != None:
        API_USER = args.username
        print("Would have set var:" + API_USER)
    gh = login(API_USER, API_KEY)
    
def makeCloneFolder(org):
    directory = os.getcwd() + "/repos"
    if org != '':
        directory += "/"+org
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def getRepoList(directory, user):
    repos = gh.repositories_by(user)
    for repo in repos:
        print(repo.as_json)
        x = repo.as_dict()["clone_url"]
        cloneRepo(x, repo.name, directory)

def cloneRepo(repo, project_name, directory):
    auth = "https://" + API_USER + ':' + API_KEY + '@'
    url = auth + repo.replace('"', '').split("https://")[1]
    print("cloning ", project_name)
    cloneCommand = "git clone " + url + " " + directory + "/" + project_name
    os.system(cloneCommand)
    
def main(args):
    setargs(args)
    print(API_KEY + " : " + API_USER)
    getRepoList(makeCloneFolder(API_USER), API_USER)
    for org in orgs:
        getRepoList(makeCloneFolder(org), org)
    


parser = argparse.ArgumentParser(description='Clone all repos from a github user')
parser.add_argument('--password', help='The password of the github account')
parser.add_argument('--username', help='The username of the github account')
args = parser.parse_args()
print(args)
main(args)