from datetime import datetime
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        login=user.login,
        project_id=user.project_id,
        env=user.env,
        domain=user.domain,
        password=models.User.set_password(user.password),
        locktime=None,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def acquire_lock(db: Session, user_id: str, user: schemas.UserLock):
    if user.locktime:
        db.query(models.User).filter(models.User.id == user_id).update(
            {"locktime": user.locktime}
        )
    else:
        db.query(models.User).filter(models.User.id == user_id).update(
            {"locktime": datetime.now()}
        )
        db.commit()
    return user


def release_lock(db: Session, user_id: str):
    db.query(models.User)\
        .filter(models.User.id == user_id).update({"locktime": None})
    db.commit()
    return
