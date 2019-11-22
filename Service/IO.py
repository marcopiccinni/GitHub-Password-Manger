# from git import Repo
from datetime import datetime
from Service import file
import threading

# Simple Git module.
# For extra function as merging, checkout or cherrypicking search online.
from brigit import Git


class GitCommandList:
    _repo = None
    _local_git_path = None
    _repo_url = None

    # to initialize the repository variable
    def init_git(self,local_git_path, repo_url):
        try:
            self._local_git_path=local_git_path
            self._repo_url=repo_url
            self._repo = Git(self._local_git_path, self._repo_url)
            self._repo.pull()
            return True
        except:
            return False

    # to make a commit, without doing a push on the remote repository on git
    def commit(self, message='Auto-commit: ' + str(datetime.now())):
        try:
            for file in local_tree(self._local_git_path):
                self._repo.add(file)
            self._repo.commit(message)
            return True
        except:
            return False

    # To push che files in the local repository.
    # A commit is generated automatically
    def push(self):
        try:

            self.commit()
            self._repo.pretty_log()
            r = self._repo.push()
            return '[*] Pushing at: ' + str(datetime.now()) + '\n' + r
        except:
            return False

    # to pull in the local from the remote repository
    def pull(self):
        try:
            self._repo.pretty_log()
            r = self._repo.pull()
            return '[*] Pulling at: ' + str(datetime.now()) + '\n' + r
        except Exception as e:
            print(e)
            return False

# function decorator to call passed function every "interval" seconds
def set_interval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop():  # executed in another thread
                while not stopped.wait(interval):  # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True  # stop if the program exits
            t.start()
            return stopped

        return wrapper

    return decorator


# To listing the local repository
def local_tree(local_git_path='C:/Users/marco/PycharmProjects/github/gitpython'):
    return file.list_file_dir(local_git_path)


''' 
# For listing files in the remote Git repository
def repo_tree(local_git_path='C:/Users/marco/PycharmProjects/github/gitpython', onlyName=False):
    repo = Repo(local_git_path)  # collegamento alla repository locale
    if onlyName:
        return [x.name for x in repo.tree().traverse()]  # Lista di cartelle e file
    return [x for x in repo.tree().traverse()]  # Lista di cartelle e file
'''
