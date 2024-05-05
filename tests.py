import datetime
import uuid
from app import schemas, crud, models
from app.database import SessionLocal


def test_get_user():
    fake_db = SessionLocal()
    fake_db.query(models.User).filter(models.User.login == "user_for_test")\
        .delete()
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
    fake_db.query(models.User).filter(models.User.login == "user_for_test")\
        .delete()
    fake_db.commit()


def test_lock():
    fake_db = SessionLocal()
    fake_db.query(models.User).filter(models.User.login == "user_for_test")\
        .delete()
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
    fake_db.query(models.User).filter(models.User.login == "user_for_test")\
        .delete()
    fake_db.commit()
