import sqlite3
import json
from openpyxl import Workbook


def export_to_excel(db_path: str, excel_path: str):
    """Экспорт данных из базы данных в Excel"""
    query = """
        SELECT
            u.telegram_id,
            u.username,
            u.first_name,
            u.last_name,
            u.language_code,
            u.registration_date,
            a.answers,
            a.payment_status,
            a.payment_id,
            a.payment_date
        FROM users u
        LEFT JOIN applications a ON u.id = a.user_id
    """

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(query).fetchall()

    wb = Workbook()
    ws = wb.active
    ws.title = "Applications"

    headers = [
        "Telegram ID", "Username", "Имя", "Фамилия", "Язык", "Дата регистрации",
        "Ответы анкеты", "Статус оплаты", "ID платежа", "Дата оплаты"
    ]
    ws.append(headers)

    for row in rows:
        row = list(row)
        # Преобразуем answers из JSON в читаемый текст
        if row[6]:  # это поле answers
            try:
                answers_dict = json.loads(row[6])
                row[6] = "\n".join(f"{k}: {v}" for k, v in answers_dict.items())
            except json.JSONDecodeError:
                row[6] = row[6]
        ws.append(row)

    # Автоподгон ширины колонок
    for col in ws.columns:
        max_length = max(len(str(cell.value) if cell.value else "") for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_length + 2

    wb.save(excel_path)
