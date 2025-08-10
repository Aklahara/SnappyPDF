import subprocess

def getGitCommit():
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    return commit