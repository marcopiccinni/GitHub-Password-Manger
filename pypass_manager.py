from Service.IO import *

_local_git_path = 'C:/Users/marco/PycharmProjects/github/gitpython'  # path assoluto repository locale
_repo_url = 'https://github.com/marcopiccinni/pypass_manager.git'
_last_update = datetime.min
_to_push = False

git = GitCommandList()
git.init_git(_local_git_path, _repo_url)


@set_interval(10)  # seconds
def t_pull():
    # La funzione permette un update temporizzato dei file
    print(git.pull())

print (git.push())

'''
# Old git version
# origin = repo.create_remote('origin', repo_url)
'''
print(git.pull())
