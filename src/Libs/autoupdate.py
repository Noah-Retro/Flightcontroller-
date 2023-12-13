import git
import json
import os

def update():   
    GITSETTINGS = json.load(open("src/settings/github.json"))
    repo = git.Repo(os.getcwd())
    repo.remotes.origin.pull()
    
if __name__ == '__main__':
    update()