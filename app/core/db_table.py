from app.schema.database import Base
from sqlalchemy import Column ,Integer ,String ,DateTime ,Boolean ,Text
from datetime import datetime

class GithubRepo(Base):
    __tablename__ = "github_repos"

    id = Column(Integer ,primary_key=True ,index=True)
    github_user = Column(String(50) ,nullable=False)
    repo_name = Column(String(100) ,nullable=False)
    repo_full_name = Column(String(100) ,nullable=False)
    description = Column(Text ,nullable=True)
    language = Column(String(100) ,nullable=True)
    forks = Column(Integer ,nullable=False)
    repo_url = Column(String(200) ,nullable=False)
    stars = Column(Integer ,nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

