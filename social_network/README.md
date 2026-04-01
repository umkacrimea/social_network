# 🌐 Social Network

> Социальная сеть на Django — платформа для общения, публикаций и взаимодействия пользователей.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.x-green?logo=django)

---

## ⚡ Быстрый старт

# 📥 1. Клонировать репозиторий

```bash
git clone git@github.com:umkacrimea/social_network.git && cd social_network
```
# 🐍 2. Создать и активировать виртуальное окружение
```bash
python3 -m venv venv
```
```
source venv/bin/activate              # Linux/macOS
# или
venv\Scripts\activate                 # Windows
```
# 📦 3. Установить зависимости
```
pip install -r requirements.txt
```
# 🗄️ 4. Настроить подключение к БД в settings.py
##    Откройте: social_network/settings.py
###    Найдите секцию DATABASES и укажите ваши параметры:
### - NAME: имя базы данных
###   - USER: пользователь БД
###    - PASSWORD: пароль
###    - HOST: хост (localhost для локальной разработки)
###    - PORT: порт (5432 для PostgreSQL, 3306 для MySQL)

# 🔄 5. Создать и применить миграции
```
python3 manage.py makemigrations
```
```
python3 manage.py migrate

```
# 👤 6. Создать суперпользователя
```
python3 manage.py createsuperuser
```

# 🚀 7. Запустить сервер разработки
python3 manage.py runserver