import requests

def fetch_github_repos(github_user):
    response = requests.get(f"https://api.github.com/users/{github_user}/repos")
    repos = response.json()

    github_repo_data_list = []

    for repo in repos :

        github_repo_data_list.append(
            {
            "github_user": github_user,
            "name" : repo["name"] , 
            "full_name" : repo["full_name"] ,
            "description" : repo["description"] ,
            "language" : repo["language"] ,
            "forks_count" : repo["forks_count"] ,
            "html_url" : repo["html_url"],
            "stargazers_count" :repo["stargazers_count"] ,
        }
        )

    return github_repo_data_list

#   wuyftomato2024