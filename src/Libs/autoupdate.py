import git
import os

def update(path:str)->None:   
    repo = git.Repo(path)
    fetch = repo.remotes.origin.pull()
    if fetch.pop != "origin/master":
        os.system('sudo reboot')

    
if __name__ == '__main__':
    repo = git.Repo(r'G:\Documente\Projekts\IDPA')
    fetch = repo.remotes.origin.fetch()
    for i in fetch:
        print(fetch.pop())

