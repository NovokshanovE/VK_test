from sqlalchemy.orm import Session

from . import models,schemas

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()

def get_users(db: Session, skip:int=0, limit:int=100):
    # return db.query(models.User).offset(skip).limit(limit).all()
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user:schemas.UserCreate):
    db_user = models.User(login=user.login,
                          project_id = user.project_id,
                          env = user.env,
                          domain = user.domain,
                          password = models.User.set_password(user.password)
                          )
    # db_user.set_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# def get_todos(db: Session, skip:int=0, limit: int=100):
#     return db.query(models.Todo).offset(skip).limit(limit).all()

# def create_user_todo(db:Session, todo:schemas.TodoCreate, user_id : int):
#     db_todo = models.Todo(**todo.model_dump(),owner_id=user_id )
#     db.add(db_todo)
#     db.commit()
#     db.refresh(db_todo)
#     return db_todo