-- ============================================================
-- ИС Учебного центра "Академия Знаний"
-- Версия: 1.0
-- СУБД: PostgreSQL 15+
-- Часть II: Создание структуры БД
-- ============================================================

-- Удаляем таблицы в порядке зависимостей (если существуют)
DROP TABLE IF EXISTS attendance, grades, schedule, students, teachers, subjects, groups, users CASCADE;

-- 1. Пользователи системы (центральная таблица авторизации)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('Администратор', 'Методист', 'Преподаватель', 'Студент')),
    is_blocked BOOLEAN NOT NULL DEFAULT FALSE,
    failed_login_attempts SMALLINT NOT NULL DEFAULT 0,
    password_must_change BOOLEAN NOT NULL DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Индекс для быстрого поиска по логину
CREATE INDEX idx_users_login ON users(login);

-- 2. Группы
CREATE TABLE groups (
    group_id SERIAL PRIMARY KEY,
    group_number VARCHAR(20) NOT NULL,
    enrollment_year INTEGER NOT NULL CHECK (enrollment_year >= 2000),
    status VARCHAR(20) NOT NULL DEFAULT 'активна' CHECK (status IN ('активна', 'выпущена'))
);

-- 3. Студенты
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    birth_date DATE CHECK (birth_date < CURRENT_DATE),
    phone VARCHAR(20) CHECK (phone ~ '^[\+\d\-\s\(\)]+$'),
    email VARCHAR(100) UNIQUE,
    group_id INTEGER REFERENCES groups(group_id) ON DELETE SET NULL
);

-- 4. Преподаватели
CREATE TABLE teachers (
    teacher_id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    degree VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

-- 5. Дисциплины
CREATE TABLE subjects (
    subject_id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    lecture_hours INTEGER NOT NULL DEFAULT 0 CHECK (lecture_hours >= 0),
    practice_hours INTEGER NOT NULL DEFAULT 0 CHECK (practice_hours >= 0),
    semester INTEGER CHECK (semester > 0)
);

-- 6. Расписание
CREATE TABLE schedule (
    lesson_id SERIAL PRIMARY KEY,
    lesson_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    classroom VARCHAR(10),
    group_id INTEGER NOT NULL REFERENCES groups(group_id) ON DELETE CASCADE,
    teacher_id INTEGER REFERENCES teachers(teacher_id) ON DELETE SET NULL,
    subject_id INTEGER NOT NULL REFERENCES subjects(subject_id) ON DELETE CASCADE,
    CONSTRAINT check_time CHECK (start_time < end_time)
);

-- 7. Успеваемость
CREATE TABLE grades (
    grade_id SERIAL PRIMARY KEY,
    score DECIMAL(5,2) NOT NULL CHECK (score >= 0 AND score <= 100),
    grade_date DATE NOT NULL DEFAULT CURRENT_DATE,
    student_id INTEGER NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    subject_id INTEGER NOT NULL REFERENCES subjects(subject_id) ON DELETE CASCADE,
    teacher_id INTEGER REFERENCES teachers(teacher_id) ON DELETE SET NULL
);

-- 8. Посещаемость
CREATE TABLE attendance (
    attendance_id SERIAL PRIMARY KEY,
    status BOOLEAN NOT NULL,
    lesson_id INTEGER NOT NULL REFERENCES schedule(lesson_id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES students(student_id) ON DELETE CASCADE,
    UNIQUE (lesson_id, student_id)
);

-- Индексы для ускорения частых запросов
CREATE INDEX idx_schedule_date ON schedule(lesson_date);
CREATE INDEX idx_grades_student ON grades(student_id);
CREATE INDEX idx_attendance_lesson ON attendance(lesson_id);