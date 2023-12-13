import git
import json
import os

def update():   
    repo = git.Repo(os.getcwd())
    repo.remotes.origin.pull()
    
if __name__ == '__main__':
    print("updating")
    update()
    print("done")