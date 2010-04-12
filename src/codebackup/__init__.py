import sys
import os
from os import path
import json
import urllib
from subprocess import call

import argparse


class User(object):
    """A registered user at a code hosting site"""
    
    def __init__(self, username, backupdir):
        self.username = username
        self.backupdir = backupdir
    
    def get_repositories(self):
        """Return the list repositories for this user"""
        j = json.load(urllib.urlopen(self.REPO_LIST_API.format(**locals())))
        return [r['name'] for r in j['repositories']]
        
    @property
    def target_dir(self):
        return path.join(self.backupdir, self.NAME)
        
    def get_repo_dir(self, repo_name):
        return path.join(self.target_dir, repo_name)
        
    def clone_repository(self, repo_name):
        assert not path.exists(self.get_repo_dir(repo_name))
        
        url = self.CLONE_URL.format(**locals())
        if not path.exists(self.target_dir):
            os.makedirs(self.target_dir)
        return call(self.CLONE_CMD.format(**locals()).split(), cwd=self.target_dir)
        
    def update_repository(self, repo_name):
        repo_dir = self.get_repo_dir(repo_name)
        print 'Backing up {0}/{1}/{2}'.format(self.NAME, self.username, repo_name)
        if not path.exists(repo_dir):
            return self.clone_repository(repo_name)
        else:
            url = self.CLONE_URL.format(**locals())
            return call(self.UPDATE_CMD.format(**locals()).split(), cwd=repo_dir)


class GithubUser(User):
    
    NAME = 'github'
    # API URL to grab repository list
    REPO_LIST_API = 'http://github.com/api/v2/json/repos/show/{self.username}'
    # github clone URL
    CLONE_URL = 'git://github.com/{self.username}/{repo_name}.git'
    CLONE_CMD = 'git clone {url}'
    UPDATE_CMD = 'git pull'
    
        
class BitbucketUser(User):
    
    NAME = 'bitbucket'
    REPO_LIST_API = 'http://api.bitbucket.org/1.0/users/{self.username}/'
    CLONE_URL = 'http://bitbucket.org/{self.username}/{repo_name}/'
    CLONE_CMD = 'hg clone {url}'
    UPDATE_CMD = 'hg pull -u'


def main():
    parser = argparse.ArgumentParser(
        description="A simple tool to backup your Github and Bitbucket repositories",
    )
    
    parser.add_argument('--github-user', type=str, help='your Github username')
    parser.add_argument('--bitbucket-user', type=str, help='your Bitbucket username')
    parser.add_argument('backupdir', type=str, 
                        help='The target backup directory')
    
    args = parser.parse_args()
    
    failed = []
    
    def backup_site(klass, username):
        u = klass(username, args.backupdir)
        for repo_name in u.get_repositories():
            ret = u.update_repository(repo_name)
            if ret:
                failed.append('{0.NAME}/{1}'.format(u, repo_name))
            
    if args.github_user:
        backup_site(GithubUser, args.github_user)
    if args.bitbucket_user:
        backup_site(BitbucketUser, args.bitbucket_user)
    
    if failed:
        print 'WARNING: the following repositories failed to update:'
        print '\n'.join(failed)
        sys.exit(2)
