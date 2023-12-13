import git
import json
import os

def update():   
    print("searching for changes in repo_")
    repo = git.Repo(os.getcwd())
    repo.remotes.origin.pull()
    print("all up to date")
    
if __name__ == '__main__':
    print("updating")
    update()
    print("done")

