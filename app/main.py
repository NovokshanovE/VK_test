from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    """Дополнительная функция для возврата текущей сессии подключения к БД

    
    """    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/create_user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Обработчик POST HTTP запросов по адресу /create_user/

    Args:
        user (schemas.UserCreate): формат данных, которые будут получены;
        db (Session, optional): база данных. Defaults to Depends(get_db).

    Raises:
        HTTPException: Возвращается ошибка 400 в случае, если user с этим login уже существует.

    Returns:
        Возвращается ответ в формате json по шаблону schemas.User.
    """    
    db_user = crud.get_user_by_login(db, login=user.login)
    if db_user:
        raise HTTPException(status_code=400, detail="login already registered")
    return crud.create_user(db=db, user=user)


@app.get("/get_users/", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Обработчик GET HTTP запросов по адресу /get_users/ для вывода всех пользователей.

    Args:
        skip (int, optional): количество пользователей которое нужно пропустить. Defaults to 0.
        limit (int, optional): какое количество пользователей стоит вывести. Defaults to 20.
        db (Session, optional): база данных. Defaults to Depends(get_db).

    Returns:
        Возвращается ответ в формате json по шаблону schemas.User.
    """    
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.post("/acquire_lock/{user_id}/")  # ,response_model=schemas.User)
def acquire_lock(user: schemas.UserLock, user_id: str, db: Session = Depends(get_db)):
    """Обработчик POSt HTTP запросов по адресу /acquire_lock/ для задания блокировки пользователя.

    Args:
        user (schemas.UserLock): Принимает Body формата json по шаблону schemas.UserLock;
        user_id (str): id пользователя, которое задается в URL запроса;
        db (Session, optional): база данных. Defaults to Depends(get_db).

    Raises:
        HTTPException: код 404, если пользователь не найден;
        HTTPException: код 405, если пользователь уже заблокирован

    Returns:
        Возвращает сообщение об успешной блокировке.
    """    
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print(db_user.locktime)

    if db_user.locktime != None and db_user.locktime > datetime.now():
        raise HTTPException(status_code=405, detail="User is lock")

    crud.acquire_lock(db, user_id, user)
    return {"detail": "Userrr"}


@app.post("/release_lock/{user_id}/")  # ,response_model=schemas.User)
def release_lock(user_id: str, db: Session = Depends(get_db)):
    """Обработчик POSt HTTP запросов по адресу /release_lock/ для задания блокировки пользователя.

    Args:
        user_id (str): id пользователя, которое задается в URL запроса;
        db (Session, optional): база данных. Defaults to Depends(get_db).

    Raises:
        HTTPException: код 404, если пользователь не найден

    Returns:
        Возвращает сообщение об успешной отмене блокировки.
    """    
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.release_lock(db, user_id)
    return {"detail": "Userrr unlock"}
