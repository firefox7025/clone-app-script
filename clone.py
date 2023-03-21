#!/usr/bin/env python

import argparse
import os
import github3
from github3 import GitHubEnterprise, login

API_PASSWORD = ''
API_USER = ''
url = 'https://api.github.com/'
org = None
gh = None

def setargs(args):
    global API_KEY
    global API_USER
    global gh
    global org
    global url
    if args.password != None:
        API_KEY = args.password
    if args.username != None:
        API_USER = args.username
    if args.url is not  None:
        url = args.url
        gh = GitHubEnterprise(url, token=API_KEY)
    else:
        gh = login(API_USER, API_KEY)
    if args.org is not None:
        org = gh.organization(args.org)

def makeCloneFolder(args):
    directory = os.getcwd() + "/repos"
    if args.org != None:
        directory += "/"+args.org
    else:
        directory += "/" + args.username
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def getRepoList(directory, user, args):
    if args.org == None:
        repos = gh.repositories_by(user)
    else:
        repos = org.repositories()
    for repo in repos:
        cloneRepo(repo, directory)

def cloneRepo(repo, directory):
    url = repo.ssh_url
    print("cloning ", repo.name)
    cloneCommand = "git clone " + url + " " + directory + "/" + repo.name
    os.system(cloneCommand)
    
def main(args):
    setargs(args)
    print(API_KEY + " : " + API_USER)
    getRepoList(makeCloneFolder(args), API_USER, args)
    


parser = argparse.ArgumentParser(description='Clone all repos from a github user')
parser.add_argument('--password', help='The password of the github account')
parser.add_argument('--username', help='The username of the github account')
parser.add_argument('--org', help='Download all of the repos of a particular org')
parser.add_argument('--url', help='The url to your version of github or GHE')
args = parser.parse_args()
print(args)
main(args)
