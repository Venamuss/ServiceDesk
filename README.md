# Service Desk

Локальное приложение УП.05 для регистрации и обработки заявок. Нужен Python 3.10 или новее; проверено с Python 3.14.10.

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver 127.0.0.1:8000
```

Откройте [127.0.0.1:8000](http://127.0.0.1:8000/). При первом запуске список пуст. Заявки сохраняются в `var/desk.sqlite3`; не удаляйте этот файл, если данные нужны. Для завершения нажмите `Ctrl+C`. Это учебный локальный запуск, не конфигурация для публикации.

**Unit-тесты**:

```bash
.venv/bin/python manage.py test desk -v 2
```