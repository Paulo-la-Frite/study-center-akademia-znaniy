-- ============================================================
-- Заполнение БД тестовыми данными
-- Пароль для всех пользователей: "123456"
-- ============================================================

-- Пользователи (пароль "123456" захеширован через bcrypt)
INSERT INTO users (login, password_hash, role, is_blocked, password_must_change) VALUES
('admin', '$2b$12$LJ3m4ys3Lk0TSwHCpFmXUu0NvtGfBzUyqZzVjO3f7yB3hKpWjA5tG', 'Администратор', FALSE, FALSE),
('metodist', '$2b$12$LJ3m4ys3Lk0TSwHCpFmXUu0NvtGfBzUyqZzVjO3f7yB3hKpWjA5tG', 'Методист', FALSE, TRUE),
('teacher_ivanova', '$2b$12$LJ3m4ys3Lk0TSwHCpFmXUu0NvtGfBzUyqZzVjO3f7yB3hKpWjA5tG', 'Преподаватель', FALSE, TRUE),
('teacher_petrov', '$2b$12$LJ3m4ys3Lk0TSwHCpFmXUu0NvtGfBzUyqZzVjO3f7yB3hKpWjA5tG', 'Преподаватель', FALSE, TRUE),
('student_smirnov', '$2b$12$LJ3m4ys3Lk0TSwHCpFmXUu0NvtGfBzUyqZzVjO3f7yB3hKpWjA5tG', 'Студент', FALSE, TRUE),
('student_kuznetsov', '$2b$12$LJ3m4ys3Lk0TSwHCpFmXUu0NvtGfBzUyqZzVjO3f7yB3hKpWjA5tG', 'Студент', FALSE, TRUE),
('student_popova', '$2b$12$LJ3m4ys3Lk0TSwHCpFmXUu0NvtGfBzUyqZzVjO3f7yB3hKpWjA5tG', 'Студент', FALSE, TRUE),
('student_sokolov', '$2b$12$LJ3m4ys3Lk0TSwHCpFmXUu0NvtGfBzUyqZzVjO3f7yB3hKpWjA5tG', 'Студент', TRUE, TRUE),
('student_volkov', '$2b$12$LJ3m4ys3Lk0TSwHCpFmXUu0NvtGfBzUyqZzVjO3f7yB3hKpWjA5tG', 'Студент', FALSE, TRUE);

-- Группы
INSERT INTO groups (group_number, enrollment_year, status) VALUES
('DPO-2024-01', 2024, 'активна'),
('DPO-2024-02', 2024, 'активна'),
('DPO-2023-01', 2023, 'выпущена'),
('DPO-2025-01', 2025, 'активна'),
('PK-2024-03', 2024, 'активна');

-- Студенты
INSERT INTO students (user_id, last_name, first_name, middle_name, birth_date, phone, email, group_id) VALUES
(5, 'Смирнов', 'Алексей', 'Игоревич', '1990-05-15', '+7-900-111-22-33', 'smirnov@mail.ru', 1),
(6, 'Кузнецов', 'Дмитрий', 'Сергеевич', '1992-08-20', '+7-900-222-33-44', 'kuznetsov@mail.ru', 1),
(7, 'Попова', 'Марина', 'Александровна', '1995-03-10', '+7-900-333-44-55', 'popova@mail.ru', 2),
(8, 'Соколов', 'Иван', 'Петрович', '1988-11-25', '+7-900-444-55-66', 'sokolov@mail.ru', 2),
(9, 'Волков', 'Артём', 'Николаевич', '1998-07-02', '+7-900-555-66-77', 'volkov@mail.ru', 4);

-- Преподаватели
INSERT INTO teachers (user_id, last_name, first_name, middle_name, degree, email) VALUES
(3, 'Иванова', 'Елена', 'Викторовна', 'Кандидат технических наук', 'ivanova_e@study.ru'),
(4, 'Петров', 'Сергей', 'Александрович', 'Доцент', 'petrov_s@study.ru');

-- Дисциплины
INSERT INTO subjects (name, lecture_hours, practice_hours, semester) VALUES
('Проектирование информационных систем', 40, 20, 1),
('Базы данных', 30, 30, 1),
('Программирование на Python', 20, 40, 1),
('Веб-разработка', 25, 35, 2),
('Информационная безопасность', 35, 25, 2);

-- Расписание
INSERT INTO schedule (lesson_date, start_time, end_time, classroom, group_id, teacher_id, subject_id) VALUES
('2026-06-16', '09:00', '10:30', '305', 1, 1, 1),
('2026-06-16', '10:45', '12:15', '305', 1, 2, 2),
('2026-06-17', '09:00', '10:30', '410', 2, 1, 3),
('2026-06-17', '10:45', '12:15', '410', 2, 2, 4),
('2026-06-18', '09:00', '10:30', '305', 1, 1, 1);

-- Успеваемость
INSERT INTO grades (score, grade_date, student_id, subject_id, teacher_id) VALUES
(85.5, '2026-06-16', 1, 1, 1),
(90.0, '2026-06-16', 2, 1, 1),
(78.0, '2026-06-17', 3, 3, 1),
(92.5, '2026-06-17', 4, 4, 2);

-- Посещаемость
INSERT INTO attendance (status, lesson_id, student_id) VALUES
(TRUE, 1, 1),
(TRUE, 1, 2),
(FALSE, 2, 1),
(TRUE, 2, 2),
(TRUE, 3, 3);