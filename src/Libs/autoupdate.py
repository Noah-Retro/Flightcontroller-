import git

def update(path:str)->None:   
    repo = git.Repo(path)
    repo.remotes.origin.pull()
    
if __name__ == '__main__':
    pass

