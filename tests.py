import datetime
import mailbox
from re import T
import uuid
import pytest
from app import schemas, crud, models
from app.database import SessionLocal
from app.main import create_user, get_db
from sqlalchemy.orm import Session
from fastapi import HTTPException
from unittest.mock import MagicMock


# def test_create_user_existing_user(mocker):
#     mock_db = MagicMock(spec=Session)
#     mock_user = schemas.UserCreate(login="existing_user", 
#                                    password="password123")
#     mocker.patch("crud.get_user_by_login", return_value=mock_user)
    
#     with pytest.raises(HTTPException) as exc_info:
#         create_user(user=mock_user, db=mock_db)
    
#     assert exc_info.value.status_code == 400
#     assert exc_info.value.detail == "login already registered"


# def test_create_user_new_user(mocker):
#     mock_db = MagicMock(spec=Session)
#     mock_user = schemas.UserCreate(login="new_user", 
#                                    password="password123")
#     mocker.patch("crud.get_user_by_login", return_value=None)
#     mocker.patch("crud.create_user", return_value=mock_user)
    
#     response = create_user(user=mock_user, db=mock_db)
    
#     assert response == mock_user


def test_get_user():
    fake_db = SessionLocal()
    fake_db.query(models.User).filter(models.User.login == "user_for_test").delete()
    fake_db.commit()
    test_user = schemas.UserCreate(login="user_for_test",
                                   project_id=uuid.UUID('b7d6519e-d1c7-481c-8b90-949aec572d26'),
                                   env="prod",
                                   domain="regular",
                                   password="test_pass")
    
    new_user = crud.create_user(fake_db, test_user)

    result = crud.get_user(fake_db, user_id=new_user.id)
    
    assert result.id == new_user.id
    assert result.login == new_user.login
    fake_db.query(models.User).filter(models.User.login == "user_for_test").delete()
    fake_db.commit()


def test_lock():
    fake_db = SessionLocal()
    fake_db.query(models.User).filter(models.User.login == "user_for_test").delete()
    fake_db.commit()
    test_user = schemas.UserCreate(login="user_for_test",
                                   project_id=uuid.UUID('b7d6519e-d1c7-481c-8b90-949aec572d26'),
                                   env="prod",
                                   domain="regular",
                                   password="test_pass")
    test_user_lock = schemas.UserLock(locktime="2024-05-06")
    
    new_user = crud.create_user(fake_db, test_user)
    crud.acquire_lock(fake_db, new_user.id, test_user_lock)
    result = crud.get_user(fake_db, user_id=new_user.id)
    
    assert result.locktime == datetime.datetime.strptime("2024-05-06", '%Y-%m-%d')
    crud.release_lock(fake_db, new_user.id)
    result = crud.get_user(fake_db, user_id=new_user.id)
    
    assert result.locktime is None
    fake_db.query(models.User).filter(models.User.login == "user_for_test").delete()
    fake_db.commit()


# def test_release_lock():
#     fake_db = SessionLocal()
#     fake_db.query(models.User).filter(models.User.login == "user_for_test").delete()
#     fake_db.commit()
#     test_user = schemas.UserCreate(login="user_for_test",
#                                    project_id=uuid.UUID('b7d6519e-d1c7-481c-8b90-949aec572d26'),
#                                    env="prod",
#                                    domain="regular",
#                                    password="test_pass")
#     # test_user_lock = schemas.UserLock(locktime="2024-05-06")
    
#     new_user = crud.create_user(fake_db, test_user)
    
