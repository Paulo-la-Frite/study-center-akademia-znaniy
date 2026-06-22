"""Конфигурация приложения."""
import os

# Параметры подключения к PostgreSQL
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'study_center',
    'user': 'postgres',
    'password': '2517Katya!'
}

# Настройки безопасности
MIN_PASSWORD_LENGTH = 6
MAX_FAILED_ATTEMPTS = 3
ACCOUNT_EXPIRY_DAYS = 30

# Название приложения
APP_NAME = "Академия Знаний"
APP_VERSION = "1.0"