"""Модуль аутентификации и управления пользователями."""
import bcrypt
from datetime import datetime, timedelta
from src import db
from src.config import MAX_FAILED_ATTEMPTS, ACCOUNT_EXPIRY_DAYS


def hash_password(password: str) -> str:
    """Хэширует пароль через bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def check_password(password: str, hashed: str) -> bool:
    """Проверяет соответствие пароля хэшу."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def authenticate(login: str, password: str) -> dict | None:
    """
    Аутентификация пользователя.
    Возвращает словарь с данными пользователя или None.
    """
    users = db.execute_query(
        "SELECT * FROM users WHERE login = %s",
        (login,),
        fetch=True
    )
    
    if not users:
        return None
    
    user = users[0]
    
    # Проверка блокировки по неактивности
    if user['last_login']:
        days_inactive = (datetime.now() - user['last_login']).days
        if days_inactive > ACCOUNT_EXPIRY_DAYS:
            db.execute_query(
                "UPDATE users SET is_blocked = TRUE WHERE user_id = %s",
                (user['user_id'],)
            )
            return {'blocked': True, 'reason': 'account_expired'}
    
    # Проверка ручной блокировки
    if user['is_blocked']:
        return {'blocked': True, 'reason': 'account_blocked'}
    
    # Проверка пароля
    if not check_password(password, user['password_hash']):
        new_attempts = user['failed_login_attempts'] + 1
        is_blocked = new_attempts >= MAX_FAILED_ATTEMPTS
        
        db.execute_query(
            "UPDATE users SET failed_login_attempts = %s, is_blocked = %s WHERE user_id = %s",
            (new_attempts, is_blocked, user['user_id'])
        )
        return None
    
    # Успешный вход
    db.execute_query(
        "UPDATE users SET failed_login_attempts = 0, last_login = %s WHERE user_id = %s",
        (datetime.now(), user['user_id'])
    )
    
    user = db.execute_query(
        "SELECT * FROM users WHERE user_id = %s",
        (user['user_id'],),
        fetch=True
    )[0]
    
    return {
        'user_id': user['user_id'],
        'login': user['login'],
        'role': user['role'],
        'password_must_change': user['password_must_change']
    }


def change_password(user_id: int, old_password: str, new_password: str) -> tuple:
    """Смена пароля. Возвращает (успех, сообщение)."""
    if len(new_password) < 6:
        return False, "Новый пароль должен содержать минимум 6 символов."
    
    users = db.execute_query(
        "SELECT password_hash FROM users WHERE user_id = %s",
        (user_id,),
        fetch=True
    )
    
    if not users:
        return False, "Пользователь не найден."
    
    if not check_password(old_password, users[0]['password_hash']):
        return False, "Неверный текущий пароль."
    
    new_hash = hash_password(new_password)
    db.execute_query(
        "UPDATE users SET password_hash = %s, password_must_change = FALSE WHERE user_id = %s",
        (new_hash, user_id)
    )
    
    return True, "Пароль успешно изменён."


def create_user(login: str, password: str, role: str) -> tuple:
    """Создание нового пользователя."""
    existing = db.execute_query(
        "SELECT user_id FROM users WHERE login = %s",
        (login,),
        fetch=True
    )
    
    if existing:
        return False, f"Пользователь с логином '{login}' уже существует."
    
    password_hash = hash_password(password)
    db.execute_query(
        "INSERT INTO users (login, password_hash, role, password_must_change) VALUES (%s, %s, %s, TRUE)",
        (login, password_hash, role)
    )
    
    return True, "Пользователь успешно создан."


def get_all_users() -> list:
    """Получение списка всех пользователей."""
    return db.execute_query(
        "SELECT user_id, login, role, is_blocked, failed_login_attempts, last_login, created_at FROM users ORDER BY user_id",
        fetch=True
    )