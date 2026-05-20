from fastapi import FastAPI ,HTTPException ,Depends
from fastapi.responses import JSONResponse
from app.repositories.repositories import get_DB_repo
from app.service.github_service import fetch_github_repos
from app.schema.database import engine ,Base ,SessionLocal
from app.service.dataSync_service import syncRepo

app = FastAPI()

# 创建所有继承自Base的所有表，路径是bind=engine这个接口
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()

@app.exception_handler(HTTPException)
def setError(request ,exc:HTTPException):
    return JSONResponse(
        status_code = exc.status_code ,
        content= {
            "status":"fail",
            "data" : None,
            "detail":exc.detail
        }
    )

@app.exception_handler(Exception)
def error(request ,exc:Exception):
    return JSONResponse(
        status_code = 500 ,
        content={
            "status":"fail",
            "data" : None,
            "detail":str(exc)
        }
    )

@app.get("/")
def index():
    return "fastapi was running"

# @app.get("/repo")
# def get_github_repo(github_user :str):
#     return fetch_github_repos(github_user)

@app.get("/old_repo")
def get_github_repo(github_user :str ,db=Depends(get_db)):
    return get_DB_repo(db ,github_user)

@app.post("/get/{github_user}")
def get_repo_name(github_user :str | None =None ,db=Depends(get_db)):
    return syncRepo(db = db,github_user =github_user)