import git
import os

def update(path:str)->None:   
    repo = git.Repo(path)
    fetch = repo.remotes.origin.pull()
    if fetch != None:
        os.system('sudo reboot')

    
if __name__ == '__main__':
    pass

