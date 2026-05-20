from fastapi import HTTPException 
from app.schema.model import apiResponse
from app.core.db_table import GithubRepo

# ***********
# 创建user
# ***********
def get_DB_repo(db ,github_user):
    old_repos_List = []

    old_repos = db.query(GithubRepo).filter(GithubRepo.github_user == github_user).all()

    for old_repo in old_repos :
        old_repos_List.append(
            {"id" : old_repo.id ,
            "github_user" : old_repo.github_user ,
            "repo_name" : old_repo.repo_name ,
            "repo_full_name" : old_repo.repo_full_name ,
            "description" : old_repo.description ,
            "language" : old_repo.language ,
            "forks" : old_repo.forks ,
            "repo_url" : old_repo.repo_url ,
            "stars" : old_repo.stars ,
            "is_deleted" : old_repo.is_deleted ,
            "updated_at" : old_repo.updated_at 
            }
        )

    return old_repos_List

def create_sql_repo(db ,github_user ,repo_name ,repo_full_name ,description ,language ,forks ,repo_url ,stars ,is_deleted):
        
    new_repo = GithubRepo(
        github_user = github_user ,
        repo_name = repo_name,
        repo_full_name = repo_full_name ,
        description = description ,
        language = language ,
        forks = forks ,
        repo_url = repo_url ,
        stars = stars ,
        is_deleted = is_deleted
    )

    db.add(new_repo)
    db.commit()
    
    return {"status" : "ok"}

def update_sqlRepo(db ,repo_full_name):
    old_repo = db.query(GithubRepo).filter(GithubRepo.repo_full_name == repo_full_name).first()

    if not old_repo :
        raise HTTPException(status_code=404 ,detail="is not repo")
    else :

        old_repo.is_deleted = True

        db.commit()

    return {"status" : "ok"}
    
def update_sqlRepoContent(db ,repo_full_name ,stars ,forks ,description ,language):
    old_repo = db.query(GithubRepo).filter(GithubRepo.repo_full_name == repo_full_name).first()

    old_repo.stars = stars
    old_repo.forks = forks
    old_repo.description = description
    old_repo.language = language

    db.commit()

    return {"status" : "ok"}
