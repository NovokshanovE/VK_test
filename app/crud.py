from datetime import datetime
from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: str):
    """Функция для получения данных о пользователе из БД по id.

    Args:
        db (Session): сессия в бд
        user_id (int): id пользователя

    Returns:
        User: Возвращает данные о пользователе
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_login(db: Session, login: str):
    """Функция для олучения данных о пользователе из БД по логину.

    Args:
        db (Session): Сессия подключения к БД
        login (str): Логин пользователя

    Returns:
        User: Возвращает данные о пользователе
    """
    return db.query(models.User).filter(models.User.login == login).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Функция для получения списка пользователей из БД

    Args:
        db (Session): Сессия подключения к БД
        skip (int, optional): Количество  пользователей, которое стоит
        пропустить. Defaults to 0.
        limit (int, optional): Количество пользователей, которое стоит вернуть.
        Defaults to 100.

    Returns:
        List[User]: возвращается список пользователей.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> schemas.User:
    """ Функция для создания пользователя по шаблону.

    Args:
        db (Session): Сессия подключения к БД
        user (schemas.UserCreate): Данные по шаблону schemas.UserCreate

    Returns:
        schemas.User: Возвращаются данные о созданном пользователе.
    """
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
    # print(db_user.id)
    return db_user


def acquire_lock(db: Session, user_id: str, user: schemas.UserLock):
    """Функция для активации блокировки пользователя по id

    Args:
        db (Session): Сессия для подключения к БД
        user_id (str): id пользователя
        user (schemas.UserLock): данные о времени, на котрое стоит
        заблокировать пользователя.
    """
    if user.locktime:
        db.query(models.User).filter(models.User.id == user_id).update(
            {"locktime": user.locktime}
        )
    else:
        db.query(models.User).filter(models.User.id == user_id).update(
            {"locktime": datetime.now()}
        )
        db.commit()
    return


def release_lock(db: Session, user_id: str):
    """Функи для деактивации блокировки

    Args:
        db (Session): _description_
        user_id (str): _description_
    """
    db.query(models.User)\
        .filter(models.User.id == user_id).update({"locktime": None})
    db.commit()
    return
