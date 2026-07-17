
from sqlalchemy import create_engine, Column, String, DateTime, Integer, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os
 
Base = declarative_base()
 
# Use DATABASE_URL from environment (Supabase/Postgres) if available,
# otherwise fall back to local SQLite for local testing only.
DATABASE_URL = os.environ.get("DATABASE_URL")
 
if DATABASE_URL:
    # Supabase URIs sometimes start with postgres:// — SQLAlchemy needs postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL)
else:
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cicd_logs.db')
    engine = create_engine(f"sqlite:///{DB_PATH}")
 
 
class FailureLog(Base):
    __tablename__ = "failure_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    repo = Column(String)
    workflow = Column(String)
    branch = Column(String)
    commit_sha = Column(String)
    failure_category = Column(String)
    root_cause = Column(Text)
    suggested_fix = Column(Text)
    confidence = Column(String)
    pr_comment_posted = Column(String, default="No")
    timestamp = Column(DateTime, default=datetime.now)
 
 
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
 
 
def log_failure(data: dict):
    session = Session()
    log = FailureLog(**data)
    session.add(log)
    session.commit()
    session.close()
 
 
def get_all_logs():
    session = Session()
    logs = session.query(FailureLog).all()
    result = [{
        "id": l.id,
        "repo": l.repo,
        "workflow": l.workflow,
        "branch": l.branch,
        "commit_sha": l.commit_sha,
        "failure_category": l.failure_category,
        "root_cause": l.root_cause,
        "suggested_fix": l.suggested_fix,
        "confidence": l.confidence,
        "pr_comment_posted": l.pr_comment_posted,
        "timestamp": l.timestamp
    } for l in logs]
    session.close()
    return result