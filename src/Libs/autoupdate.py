import git
import os

def update(path:str)->None:   
    repo = git.Repo(path)
    head = repo.head.ref
    tracking = head.tracking_branch()
    s = list(tracking.iter_items(repo,f'{head.path}..{tracking.path}'))
    
    repo.remotes.origin.pull()
    
    if len(s)>=1:
        os.system('sudo reboot')

    
if __name__ == '__main__':
    pass

