import os
import shutil
import git

local_path = "D:/.../dir"
writer_name = input("Your username: ")
writer_email = input("Your email: ")
github_username = input("GitHub username: ")

def clone_repo(repo_url):
    repo_name = repo_url.split("/")[-1]
    clone_dir = "{}/{}".format(local_path, repo_name)
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
        print(f"The directory '{clone_dir}' has been deleted.")

    print("Cloning repo", repo_url)
    repo = git.Repo.clone_from(repo_url, clone_dir)
    return repo

def change_writer(repo):
    print("Changing the writer")
    os.chdir(repo.working_dir)
    os.system("git filter-branch -f --env-filter "
            "\"GIT_AUTHOR_NAME='{}'; "
            "GIT_AUTHOR_EMAIL='{}'; "
            "GIT_COMMITTER_NAME='{}'; "
            "GIT_COMMITTER_EMAIL='{}';\" "
            " HEAD".format(writer_name, writer_email, writer_name, writer_email))

def push(repo, repo_name):
    print("Pushing changes to the destination repository...")
    
    os.chdir(repo.working_dir)
    # Remove the existing remote origin
    os.system("git remote remove origin")
    os.system("git remote add origin https://{}@github.com/{}/{}.git".format(github_username, github_username, repo_name))
    branch_name = os.popen('git rev-parse --abbrev-ref HEAD').read().strip()

    # Determine the branch to push
    if branch_name == "master":
        os.system("git push -u origin master")
    elif branch_name == "main":
        os.system("git push -u origin main")
    else:
        print(f"Branch '{branch_name}' is not supported for push.")

def main():
    repo_list = []
    with open("list.txt", 'r') as file:
        for line in file:
            repo_url = line.strip()  # Remove any leading/trailing whitespace
            if repo_url:  # Check if the line is not empty
                repo_list.append(repo_url)
    
    for repo_url in repo_list:
        repo_name = repo_url.split("/")[-1]
        repo = clone_repo(repo_url)
        change_writer(repo)
        push(repo, repo_name)

if __name__ == "__main__":
    main()