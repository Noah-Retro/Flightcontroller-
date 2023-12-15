import git
import os

def update(path:str)->None:   
    repo = git.Repo(path)
    repo.remote().fetch()
    head = repo.head.ref
    tracking = head.tracking_branch()
    s = list(tracking.iter_items(repo,f'{head.path}..{tracking.path}'))
    
    if len(s)>=1:
        repo.remotes.origin.pull()
        os.system('sudo reboot')
    

    
if __name__ == '__main__':
    repo = git.Repo(r'G:\Documente\Projekts\IDPA')
    head = repo.head.ref
    tracking = head.tracking_branch()
    s = list(tracking.iter_items(repo,f'{head.path}..{tracking.path}'))
    
    repo.remotes.origin.pull()
    
    if len(s)>=1:
        print("reboot")
        

    print("Nothing")