# Тестовое задание ВК (разработчик ПО)

## Локальный запуск

Для локального запуска должна быть установлена СУБД PostgreSQL версии 14 или выше, а так же создана БД `bot_farm`.

Для запуска сервиса необходимо прописать следующие команды:
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```


## Docker-compose


Для запуска сервиса необходимо прописать следующие команды:
```bash
docker-compose up -d
```

Для удаления необходимо прописать следующие команды:
```bash
docker compose down --rmi all -v --remove-orphans
```
