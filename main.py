import time
import gspread
import re
from oauth2client.service_account import ServiceAccountCredentials

# 🔹 Parameters (modifiable)
LANGUAGE = "ru"  # Set to "ru" for Russian, "en" for English
CREDENTIALS_FILE = 'loyal-world-419700-790e33c64829.json'  # JSON with credentials
SPREADSHEET_ID = '1j6397TPMgPSD2WbECDnq9B-vT9q9VBcih6AyWD4Y624'  # Google Sheet ID
SHEET_ID = 0  # Specific sheet (list) ID (default is the first sheet)
TEXT = "Surname"  # Text to be written
CHECK_PREFIX = "Surn"  # Prefix to check (e.g., "Surn", "ABC")
PRIORITY_CELLS = ['B3', 'B8', 'B6', 'B12', 'B17']  # Priority cells

# Language-based messages
MESSAGES = {
    "en": {
        "auth_error": "❌ API authorization error: {}. Retrying in 2 seconds...",
        "access_granted": "✅ Write access granted!",
        "read_only": "🔒 Read-only access. Waiting 1 second...",
        "api_error": "❌ API error: {}. Retrying in 2 seconds...",
        "unknown_error": "⚠️ Unknown error: {}. Retrying in 2 seconds...",
        "current_values": "\n📋 Current cell values:",
        "already_exists": "🎉 '{}' is already present. Stopping.",
        "written": "✅ Successfully written '{}' to {}",
        "check_again": "🔄 Checking access again in 1 second...",
        "checking_access": "🔄 Checking for edit access...",
        "recorded": "🎉 Successfully recorded '{}' in {}. Stopping.",
        "prefix_found": "🔄 '{}' detected in {}, completing with '{}'...",
        "removed": "⚠️ '{}' was removed from {}, trying the next available cell."
    },
    "ru": {
        "auth_error": "❌ Ошибка API при авторизации: {}. Повтор через 2 секунды...",
        "access_granted": "✅ Доступ к записи есть!",
        "read_only": "🔒 Доступ только для чтения. Ждем 1 секунду...",
        "api_error": "❌ Ошибка API: {}. Повтор через 2 секунды...",
        "unknown_error": "⚠️ Неизвестная ошибка: {}. Повтор через 2 секунды...",
        "current_values": "\n📋 Текущие значения ячеек:",
        "already_exists": "🎉 '{}' уже есть. Остановка.",
        "written": "✅ Записали '{}' в {}",
        "check_again": "🔄 Проверяем доступ снова через 1 секунду...",
        "checking_access": "🔄 Проверяем доступ к редактированию...",
        "recorded": "🎉 Полностью записано '{}' в {}. Остановка.",
        "prefix_found": "🔄 '{}' записано в {}, дописываем '{}'...",
        "removed": "⚠️ '{}' удалено из {}, пробуем следующую ячейку."
    }
}

def authorize_google_sheets():
    """Authorize Google Sheets API with error handling"""
    while True:
        try:
            scope = ["https://www.googleapis.com/auth/spreadsheets"]
            credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
            client = gspread.authorize(credentials)
            return client.open_by_key(SPREADSHEET_ID).get_worksheet_by_id(SHEET_ID)
        except Exception as e:
            print(MESSAGES[LANGUAGE]["auth_error"].format(e))
            time.sleep(2)

def has_edit_access(worksheet):
    """Check write access (if we can add a row, we can write)"""
    while True:
        try:
            test_row = ["Access check"] if LANGUAGE == "en" else ["Проверка доступа"]
            worksheet.append_row(test_row)
            print(MESSAGES[LANGUAGE]["access_granted"])
            return True
        except gspread.exceptions.APIError as e:
            if e.response.status_code == 403:
                print(MESSAGES[LANGUAGE]["read_only"])
                time.sleep(1)
            else:
                print(MESSAGES[LANGUAGE]["api_error"].format(e))
                time.sleep(2)
        except Exception as e:
            print(MESSAGES[LANGUAGE]["unknown_error"].format(e))
            time.sleep(2)

def is_empty(value):
    """Check if a cell is 'empty' (null, spaces, or only symbols)."""
    return value is None or value.strip() == "" or re.fullmatch(r"[\W_]+", value.strip()) is not None

def get_values(worksheet):
    """Retrieve values of priority cells (with API error handling)"""
    while True:
        try:
            values = worksheet.batch_get(PRIORITY_CELLS)
            return {cell: (values[i][0][0] if values[i] else '') for i, cell in enumerate(PRIORITY_CELLS)}
        except gspread.exceptions.APIError as e:
            print(MESSAGES[LANGUAGE]["api_error"].format(e))
            time.sleep(2)
        except Exception as e:
            print(MESSAGES[LANGUAGE]["unknown_error"].format(e))
            time.sleep(2)

def update_cell(worksheet, cell):
    """Update a cell (with API error handling)"""
    while True:
        try:
            worksheet.update(cell, [[TEXT]])
            print(MESSAGES[LANGUAGE]["written"].format(TEXT, cell))
            return
        except gspread.exceptions.APIError as e:
            print(MESSAGES[LANGUAGE]["api_error"].format(e))
            time.sleep(2)
        except Exception as e:
            print(MESSAGES[LANGUAGE]["unknown_error"].format(e))
            time.sleep(2)

def check_and_update(worksheet):
    """Main logic: checks access and writes TEXT into the first available cell"""
    while True:
        print(MESSAGES[LANGUAGE]["checking_access"])
        if has_edit_access(worksheet):
            cell_values = get_values(worksheet)
            print(MESSAGES[LANGUAGE]["current_values"], cell_values)

            # Stop if TEXT is already in one of the cells
            if any(value.strip() == TEXT for value in cell_values.values()):
                print(MESSAGES[LANGUAGE]["already_exists"].format(TEXT))
                return

            # Find the first suitable cell for writing
            for cell in PRIORITY_CELLS:
                value = cell_values[cell].strip()
                
                if is_empty(value) or value == CHECK_PREFIX:
                    update_cell(worksheet, cell)

                    # Verify if TEXT was successfully written
                    time.sleep(1)
                    new_value = worksheet.acell(cell).value.strip()
                    
                    if new_value == TEXT:
                        print(MESSAGES[LANGUAGE]["recorded"].format(TEXT, cell))
                        return
                    elif new_value.startswith(CHECK_PREFIX):
                        print(MESSAGES[LANGUAGE]["prefix_found"].format(CHECK_PREFIX, cell, TEXT))
                        update_cell(worksheet, cell)
                        time.sleep(1)
                        if worksheet.acell(cell).value.strip() == TEXT:
                            print(MESSAGES[LANGUAGE]["recorded"].format(TEXT, cell))
                            return
                    else:
                        print(MESSAGES[LANGUAGE]["removed"].format(TEXT, cell))
                        continue

        print(MESSAGES[LANGUAGE]["check_again"])
        time.sleep(1)

if __name__ == "__main__":
    print(f"🔹 SPREADSHEET_ID: {SPREADSHEET_ID}")
    print(f"🔹 SHEET_ID: {SHEET_ID}")
    print(f"🔹 TEXT: {TEXT}")
    print(f"🔹 CHECK_PREFIX: {CHECK_PREFIX}")

    worksheet = authorize_google_sheets()
    check_and_update(worksheet)
