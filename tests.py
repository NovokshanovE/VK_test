import pytest
from app import schemas, crud
from app.main import create_user
from sqlalchemy.orm import Session
from fastapi import HTTPException
from unittest.mock import MagicMock

def test_create_user_existing_user(mocker):
    mock_db = MagicMock(spec=Session)
    mock_user = schemas.UserCreate(login="existing_user", 
                                   password="password123")
    mocker.patch("crud.get_user_by_login", return_value=mock_user)
    
    with pytest.raises(HTTPException) as exc_info:
        create_user(user=mock_user, db=mock_db)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "login already registered"

def test_create_user_new_user(mocker):
    mock_db = MagicMock(spec=Session)
    mock_user = schemas.UserCreate(login="new_user", 
                                   password="password123")
    mocker.patch("crud.get_user_by_login", return_value=None)
    mocker.patch("crud.create_user", return_value=mock_user)
    
    response = create_user(user=mock_user, db=mock_db)
    
    assert response == mock_user
