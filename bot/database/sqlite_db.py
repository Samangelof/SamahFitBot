# import sqlite3
# import json
# from typing import Optional, Tuple, List, Any, Dict
# from datetime import datetime, timedelta


# class DatabaseManager:
#     def __init__(self, db_path: str):
#         self.db_path = db_path
#         self._create_tables()

#     def _create_tables(self):
#         """Создание необходимых таблиц"""
#         with sqlite3.connect(self.db_path) as conn:
#             cursor = conn.cursor()
            
#             # Таблица пользователей
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS users (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     telegram_id INTEGER UNIQUE NOT NULL,
#                     username TEXT,
#                     first_name TEXT,
#                     last_name TEXT,
#                     language_code TEXT,
#                     registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             ''')
            
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS user_access (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     user_id INTEGER NOT NULL,
#                     access_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Время начала доступа
#                     access_end TIMESTAMP,  -- Время окончания доступа (через 30 дней)
#                     FOREIGN KEY (user_id) REFERENCES users(id)
#                 )
#             ''')
            
#             # Таблица заявок
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS applications (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     user_id INTEGER NOT NULL,
#                     answers TEXT NOT NULL,  -- JSON строка со всеми ответами анкеты
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     payment_status TEXT DEFAULT 'не оплачено',
#                     payment_id TEXT,
#                     payment_url TEXT,
#                     payment_date TIMESTAMP,
#                     FOREIGN KEY (user_id) REFERENCES users(id)
#                 )
#             ''')

#             # Таблица посещений
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS user_visits (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     telegram_id INTEGER NOT NULL,
#                     username TEXT,
#                     first_name TEXT,
#                     last_name TEXT,
#                     visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             ''')

#             # Таблица рефералов
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS referrals (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     user_id INTEGER NOT NULL,
#                     invited_user_id INTEGER NOT NULL,
#                     paid INTEGER DEFAULT 0,
#                     discount_applied INTEGER DEFAULT 0,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#                 )
#             ''')
            
#             cursor.execute('''
#                 CREATE TABLE IF NOT EXISTS promocodes (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     code TEXT UNIQUE NOT NULL,
#                     discount_percent INTEGER NOT NULL,
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     is_active INTEGER DEFAULT 1
#                 )
#             ''')

#             conn.commit()

    # def add_user_if_not_exists(self, user):
    #     with sqlite3.connect(self.db_path) as conn:
    #         cursor = conn.cursor()
    #         cursor.execute('''
    #             INSERT OR IGNORE INTO users (telegram_id, username, first_name, last_name, language_code)
    #             VALUES (?, ?, ?, ?, ?)
    #         ''', (user.id, user.username, user.first_name, user.last_name, user.language_code))
    #         conn.commit()

    # def add_access(self, user_id):
    #     """Добавляет доступ пользователю на 30 дней после оплаты"""
    #     with sqlite3.connect(self.db_path) as conn:
    #         cursor = conn.cursor()
            
    #         # Вычисляем дату окончания доступа (через 30 дней)
    #         access_end = datetime.now() + timedelta(days=30)
            
    #         # Добавляем запись в таблицу user_access
    #         cursor.execute('''
    #             INSERT INTO user_access (user_id, access_end)
    #             VALUES (?, ?)
    #         ''', (user_id, access_end))
            
    #         conn.commit()

    # def check_access(self, user_id):
    #     """Проверяет, есть ли у пользователя доступ"""
    #     with sqlite3.connect(self.db_path) as conn:
    #         cursor = conn.cursor()
            
    #         # Проверяем, есть ли доступ и не истёк ли он
    #         cursor.execute('''
    #             SELECT access_end FROM user_access
    #             WHERE user_id = ? AND access_end > CURRENT_TIMESTAMP
    #         ''', (user_id,))
    #         access = cursor.fetchone()
            
    #         if access:
    #             return True  # Доступ ещё не истёк
    #         return False  # Доступ истёк или не найден


    # def log_user_visit(self, user):
    #     """Логирование посещения пользователя"""
    #     with sqlite3.connect(self.db_path) as conn:
    #         cursor = conn.cursor()
    #         cursor.execute('''
    #             INSERT INTO user_visits (telegram_id, username, first_name, last_name)
    #             VALUES (?, ?, ?, ?)
    #         ''', (user.id, user.username, user.first_name, user.last_name))
    #         conn.commit()

    # def get_daily_visits(self):
    #     """Получить количество визитов по дням"""
    #     with sqlite3.connect(self.db_path) as conn:
    #         cursor = conn.cursor()
    #         cursor.execute('''
    #             SELECT DATE(visit_time) as visit_date, COUNT(*) as visit_count
    #             FROM user_visits
    #             GROUP BY visit_date
    #             ORDER BY visit_date DESC
    #             LIMIT 30
    #         ''')
    #         return cursor.fetchall()

    # def get_unique_user_count(self):
    #     """Получить общее количество уникальных пользователей"""
    #     with sqlite3.connect(self.db_path) as conn:
    #         cursor = conn.cursor()
    #         cursor.execute('''
    #             SELECT COUNT(DISTINCT telegram_id) FROM user_visits
    #         ''')
    #         result = cursor.fetchone()
    #         return result[0] if result else 0



    # def add_referral(self, inviter_telegram_id: int, invited_telegram_id: int):
    #     """Записывает нового реферала"""
    #     with sqlite3.connect(self.db_path) as conn:
    #         cursor = conn.cursor()
            
    #         # Получаем user_id по telegram_id пригласившего
    #         cursor.execute('SELECT id FROM users WHERE telegram_id = ?', (inviter_telegram_id,))
    #         inviter_row = cursor.fetchone()
    #         if not inviter_row:
    #             return  # Пригласивший не найден — пропускаем
    #         inviter_id = inviter_row[0]

    #         # Получаем user_id по telegram_id приглашённого
    #         cursor.execute('SELECT id FROM users WHERE telegram_id = ?', (invited_telegram_id,))
    #         invited_row = cursor.fetchone()
    #         if not invited_row:
    #             return  # Приглашённый не найден — пропускаем
    #         invited_id = invited_row[0]

    #         # Проверяем чтобы не было дубликатов
    #         cursor.execute('''
    #             SELECT id FROM referrals 
    #             WHERE user_id = ? AND invited_user_id = ?
    #         ''', (inviter_id, invited_id))
    #         if cursor.fetchone():
    #             return  # Уже записан — пропускаем

    #         # Записываем реферала
    #         cursor.execute('''
    #             INSERT INTO referrals (user_id, invited_user_id) 
    #             VALUES (?, ?)
    #         ''', (inviter_id, invited_id))

    #         conn.commit()


    # def get_referral_count(self, telegram_id: int) -> int:
    #     with sqlite3.connect(self.db_path) as conn:
    #         cursor = conn.cursor()

    #         cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (telegram_id,))
    #         user_row = cursor.fetchone()
    #         if not user_row:
    #             return 0
    #         user_id = user_row[0]

    #         cursor.execute("SELECT COUNT(*) FROM referrals WHERE user_id = ? AND paid = 1", (user_id,))
    #         count = cursor.fetchone()[0]
    #         return count


    # def get_discount_percent(self, telegram_id: int) -> int:
    #     count = self.get_referral_count(telegram_id)
    #     if count >= 2:
    #         return 50
    #     elif count == 1:
    #         return 25
    #     else:
    #         return 0




    # def execute_query(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[List[Tuple]]:
    #     """
    #     Выполняет SQL-запрос с параметрами.
    #     :param query: SQL-запрос для выполнения.
    #     :param params: Кортеж с параметрами для подстановки в запрос.
    #     :return: Список кортежей с результатами запроса (только для SELECT).
    #     """
    #     try:
    #         with sqlite3.connect(self.db_path) as conn:
    #             cursor = conn.cursor()
    #             if params:
    #                 cursor.execute(query, params)
    #             else:
    #                 cursor.execute(query)
    #             # Если это SELECT-запрос, возвращаем результаты
    #             if query.strip().upper().startswith("SELECT"):
    #                 return cursor.fetchall()
    #             # Иначе просто фиксируем изменения
    #             conn.commit()
    #             return None
    #     except sqlite3.Error as e:
    #         print(f"Ошибка выполнения SQL-запроса: {e}")
    #         return None

    # def add_user(self, telegram_id: int, username: Optional[str] = None, 
    #             first_name: Optional[str] = None, last_name: Optional[str] = None, 
    #             language_code: Optional[str] = None) -> int:
    #     """
    #     Добавляет пользователя в базу данных или обновляет его данные, если он уже существует.
    #     :return: ID пользователя в базе данных
    #     """
    #     try:
    #         with sqlite3.connect(self.db_path) as conn:
    #             cursor = conn.cursor()
                
    #             # Проверяем, существует ли пользователь
    #             cursor.execute('SELECT id FROM users WHERE telegram_id = ?', (telegram_id,))
    #             user = cursor.fetchone()
                
    #             if user:
    #                 # Обновляем данные существующего пользователя
    #                 cursor.execute(
    #                     'UPDATE users SET username = ?, first_name = ?, last_name = ?, language_code = ? WHERE telegram_id = ?',
    #                     (username, first_name, last_name, language_code, telegram_id)
    #                 )
    #                 return user[0]  # Возвращаем существующий ID
    #             else:
    #                 # Добавляем нового пользователя
    #                 cursor.execute(
    #                     'INSERT INTO users (telegram_id, username, first_name, last_name, language_code) VALUES (?, ?, ?, ?, ?)',
    #                     (telegram_id, username, first_name, last_name, language_code)
    #                 )
    #                 return cursor.lastrowid  # Возвращаем новый ID
    #     except sqlite3.Error as e:
    #         print(f"Ошибка при добавлении/обновлении пользователя: {e}")
    #         return 0

    # def save_application(self, telegram_id: int, answers: Dict) -> int:
    #     """
    #     Сохраняет заявку пользователя в базу данных.
    #     :param telegram_id: Telegram ID пользователя
    #     :param answers: Словарь с ответами анкеты
    #     :return: ID заявки или 0 в случае ошибки
    #     """
    #     try:
    #         with sqlite3.connect(self.db_path) as conn:
    #             cursor = conn.cursor()
                
    #             # Получаем ID пользователя из таблицы users
    #             cursor.execute('SELECT id FROM users WHERE telegram_id = ?', (telegram_id,))
    #             user_result = cursor.fetchone()
                
    #             if not user_result:
    #                 print(f"Пользователь с telegram_id {telegram_id} не найден в базе")
    #                 return 0
                
    #             user_id = user_result[0]
    #             answers_json = json.dumps(answers, ensure_ascii=False)
                
    #             # Сохраняем заявку
    #             cursor.execute(
    #                 'INSERT INTO applications (user_id, answers) VALUES (?, ?)',
    #                 (user_id, answers_json)
    #             )
                
    #             return cursor.lastrowid
    #     except sqlite3.Error as e:
    #         print(f"Ошибка при сохранении заявки: {e}")
    #         return 0

    # def mark_referral_paid(self, invited_telegram_id: int):
    #     with sqlite3.connect(self.db_path) as conn:
    #         cursor = conn.cursor()
    #         # Получаем user_id приглашённого
    #         cursor.execute("SELECT id FROM users WHERE telegram_id = ?", (invited_telegram_id,))
    #         row = cursor.fetchone()
    #         if not row:
    #             return
    #         invited_user_id = row[0]
    #         # Помечаем рефералку как оплаченную
    #         cursor.execute(
    #             "UPDATE referrals SET paid = 1 WHERE invited_user_id = ?",
    #             (invited_user_id,)
    #         )
    #         conn.commit()

    # def update_payment_url(self, application_id: int, payment_url: str):
    #     with sqlite3.connect(self.db_path) as conn:
    #         cursor = conn.cursor()
    #         cursor.execute(
    #             "UPDATE applications SET payment_url = ? WHERE id = ?",
    #             (payment_url, application_id)
    #         )
    #         conn.commit()


    # def update_payment_status(self, application_id: int, payment_status: str, payment_id: Optional[str] = None) -> bool:
    #     """
    #     Обновляет статус оплаты заявки.
    #     :param application_id: ID заявки
    #     :param payment_status: Статус оплаты ('оплачено', 'не оплачено', 'ошибка')
    #     :param payment_id: ID платежа (если есть)
    #     :return: True если успешно, иначе False
    #     """
    #     try:
    #         with sqlite3.connect(self.db_path) as conn:
    #             cursor = conn.cursor()
                
    #             now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
    #             if payment_status == 'оплачено':
    #                 cursor.execute(
    #                     'UPDATE applications SET payment_status = ?, payment_id = ?, payment_date = ? WHERE id = ?',
    #                     (payment_status, payment_id, now, application_id)
    #                 )
    #                 cursor.execute('SELECT user_id FROM applications WHERE id = ?', (application_id,))
    #                 user_id = cursor.fetchone()[0]
    #                 self.add_user_access(user_id) 

    #                 # -----------------------------------
    #                 cursor.execute('SELECT telegram_id FROM users WHERE id = ?', (user_id,))
    #                 telegram_row = cursor.fetchone()
    #                 if telegram_row:
    #                     telegram_id = telegram_row[0]
    #                     self.mark_referral_paid(telegram_id)
    #                 # -----------------------------------

    #             else:
    #                 cursor.execute(
    #                     'UPDATE applications SET payment_status = ?, payment_id = ? WHERE id = ?',
    #                     (payment_status, payment_id, application_id)
    #                 )
                
    #             return True
    #     except sqlite3.Error as e:
    #         print(f"Ошибка при обновлении статуса оплаты: {e}")
    #         return False

    # def get_application_by_id(self, application_id: int) -> Optional[Dict]:
    #     """
    #     Получает данные заявки по ID.
    #     :return: Словарь с данными заявки или None
    #     """
    #     try:
    #         with sqlite3.connect(self.db_path) as conn:
    #             conn.row_factory = sqlite3.Row  # Чтобы получать результаты в виде словарей
    #             cursor = conn.cursor()
                
    #             cursor.execute('''
    #                 SELECT a.*, u.telegram_id, u.username, u.first_name, u.last_name
    #                 FROM applications a
    #                 JOIN users u ON a.user_id = u.id
    #                 WHERE a.id = ?
    #             ''', (application_id,))
                
    #             row = cursor.fetchone()
    #             if not row:
    #                 return None
                
    #             result = dict(row)
    #             result['answers'] = json.loads(result['answers'])
    #             return result
    #     except sqlite3.Error as e:
    #         print(f"Ошибка при получении заявки: {e}")
    #         return None

    # def get_user_applications(self, telegram_id: int) -> List[Dict]:
    #     """
    #     Получает все заявки пользователя.
    #     :return: Список словарей с данными заявок
    #     """
    #     try:
    #         with sqlite3.connect(self.db_path) as conn:
    #             conn.row_factory = sqlite3.Row
    #             cursor = conn.cursor()
                
    #             cursor.execute('''
    #                 SELECT a.*
    #                 FROM applications a
    #                 JOIN users u ON a.user_id = u.id
    #                 WHERE u.telegram_id = ?
    #                 ORDER BY a.created_at DESC
    #             ''', (telegram_id,))
                
    #             rows = cursor.fetchall()
    #             result = []
                
    #             for row in rows:
    #                 app_data = dict(row)
    #                 app_data['answers'] = json.loads(app_data['answers'])
    #                 result.append(app_data)
                
    #             return result
    #     except sqlite3.Error as e:
    #         print(f"Ошибка при получении заявок пользователя: {e}")
    #         return []
        

    # def get_telegram_id_by_application_id(self, application_id: int) -> Optional[int]:
    #     """
    #     Получает telegram_id пользователя по ID заявки.
    #     :param application_id: ID заявки
    #     :return: telegram_id или None если не найден
    #     """
    #     try:
    #         with sqlite3.connect(self.db_path) as conn:
    #             cursor = conn.cursor()
                
    #             cursor.execute('''
    #                 SELECT u.telegram_id
    #                 FROM applications a
    #                 JOIN users u ON a.user_id = u.id
    #                 WHERE a.id = ?
    #             ''', (application_id,))
                
    #             result = cursor.fetchone()
    #             return result[0] if result else None
    #     except sqlite3.Error as e:
    #         print(f"Ошибка при получении telegram_id: {e}")
    #         return None