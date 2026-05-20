from app.repositories.repositories import get_DB_repo ,create_sql_repo ,update_sqlRepo ,update_sqlRepoContent
from app.service.github_service import fetch_github_repos
from app.mock_data.gitRepo_mock_data import get_mock_repos

def syncRepo(db ,github_user):
    sql_repos = get_DB_repo(db ,github_user)
    git_repos = fetch_github_repos(github_user)
    # git_repos = get_mock_repos()

    sql_repo_map = {}
    git_repo_map = {} 

    created_count = 0
    updated_count = 0
    deleted_count = 0

    for sql_repo in sql_repos :

        sql_repo_name = sql_repo["repo_full_name"]
        sql_repo_map[sql_repo_name] = sql_repo

        # print(sql_repo_map[sql_repo_name]) 

    for git_repo in git_repos:

        full_name = git_repo["full_name"]
        name = git_repo["name"]
        description = git_repo["description"]
        language = git_repo["language"]
        forks_count = git_repo["forks_count"]
        html_url = git_repo["html_url"]
        stargazers_count = git_repo["stargazers_count"]

        git_repo_map[full_name] = git_repo

        if full_name not in sql_repo_map :
            create_sql_repo(
                db = db ,
                github_user = github_user,
                repo_name = name,
                repo_full_name = full_name,
                description = description,
                language = language,
                forks = forks_count,
                repo_url = html_url,
                stars = stargazers_count,
                is_deleted = False
                )
            
            created_count += 1
        else :
            if (sql_repo_map[full_name]["stars"] != stargazers_count 
                or sql_repo_map[full_name]["forks"] != forks_count 
                or sql_repo_map[full_name]["description"] != description 
                or sql_repo_map[full_name]["language"] != language
                ):
                update_sqlRepoContent(
                    db = db ,
                    repo_full_name = full_name ,
                    stars = stargazers_count ,
                    forks = forks_count ,
                    description = description ,
                    language = language
                    )
                
                updated_count += 1

    for sql_repo in sql_repos :
        sql_repo_name = sql_repo["repo_full_name"]
        if sql_repo_name not in git_repo_map :
            update_sqlRepo(db=db, repo_full_name=sql_repo_name)
            deleted_count += 1

    return ({"status" : "ok" ,
             "created_count" : created_count ,
             "updated_count" : updated_count ,
             "deleted_count" : deleted_count
             })



        