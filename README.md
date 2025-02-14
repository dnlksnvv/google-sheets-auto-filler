# 📊 Google Sheets Auto-Filler

**EN**

**Google Sheets Auto-Filler** is a Python script that automatically checks for editing access to a Google Sheets document, retrieves data from priority cells, and writes to the first available cell with the specified text. If the data is not saved, the script retries until the write operation is successful.

The script is designed for automatic filling of Google Sheets with an editing access waiting function.

### 📌 Example Use Case

Imagine you need to select a topic for your coursework. There are 100 students and 100 available topics, with each student getting one topic. Among these, only one is suitable for you.

Your instructor publishes 100 topics in a **read-only** Google Sheet. At an unspecified (or predetermined) time, the sheet will be opened for editing, allowing you to select a topic. **This script provides an advantage over other participants** by checking for edit access every second. Once access is detected, it checks priority cells in descending order of priority:

```python
PRIORITY_CELLS = ["A1", "A2", "A3", ..., "A9"]
# A1 - Best topic (highest priority)
# A9 - Worst topic (lowest priority)
```

The script will attempt to write your **TEXT** (topic number or surname) **to the highest-priority available cell**, which:

- Is **empty** (null, spaces, or symbols—without letters or numbers)
- **Contains the CHECK_PREFIX value**

If **CHECK_PREFIX = "John"**, and a cell contains "John" or is empty, the script writes your **TEXT** to it. If the cell contains something else (e.g., "Kriss" or "123"), the script moves to the next priority cell.

---

## 🚀 Features

- ✅ Automatically retrieves data from specified Google Sheets cells.
- ✅ Checks for edit access.
- ✅ Writes specified **text** to the first available cell.
- ✅ Allows modification of **spreadsheet ID** and **specific sheet ID**.
- ✅ Configurable **data validation threshold** (e.g., if the text is shorter than 3 characters or contains only symbols).
- ✅ Handles **API errors** (waits and retries if the API is temporarily unavailable).
- ✅ Supports **two languages** (English/Russian) by changing the `LANGUAGE` variable.

---

## 🛠️ Installation and Setup

### **1️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```


### **2️⃣ Create a Google API Account and Download JSON Credentials**

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the Google Sheets API.
3. Create a service account and download the JSON credentials file.
4. Add the service account email to Google Sheets as an **Editor**.

### **3️⃣ Save the JSON Credentials File**

Place the JSON file (e.g., `credentials.json`) in the project's root directory.

### **4️⃣ Configure Variables in `config.py`**

```python
CREDENTIALS_FILE = 'credentials.json'  # Credentials file
SPREADSHEET_ID = 'your_spreadsheet_id'  # Google Sheets ID
SHEET_ID = 0  # Specific sheet ID (0 = first sheet)
TEXT = "Last Name First Name"  # Text to be written
CHECK_PREFIX = "Last"  # Prefix to check (e.g., "John")
PRIORITY_CELLS = ['B3', 'B8', 'B6', 'B12', 'B17']  # Priority cells
LANGUAGE = "en"  # Language: "en" or "ru"
```

### 🔍 How to Get `SPREADSHEET_ID` and `SHEET_ID`?

- **SPREADSHEET_ID** can be found in the Google Sheets URL:
  ```
  https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID/edit#gid=0
  ```
- **SHEET_ID** is the number after `gid=` in the URL:
  ```
  https://docs.google.com/spreadsheets/d/58nhlnFIUZBPNfPWrJYKhkdvm-8fPb2CKbdOLUxiO1nap/htmlview?gid=0#gid=0
  ```
  In this example, `SHEET_ID = 0`.

---

## 🔄 How the Script Works

1️⃣ **Checks for access** to the sheet (reader or editor).
2️⃣ **Retrieves data** from priority cells.
3️⃣ If **"TEXT" is already recorded** in one of the cells — **the script stops**.
4️⃣ **Cells are processed in priority order**. The text is written to **the first suitable cell**, which:

- Is **empty**.
- Contains **CHECK_PREFIX** (e.g., if `CHECK_PREFIX = "12345"`, **it will write to a cell with "12345"**).

5️⃣ If **after writing, only CHECK_PREFIX remains** (e.g., "John") — **it completes the full text**.
6️⃣ If the text is removed **after insertion** — it tries the next available cell.

---

## 🏃 Running the Script

```bash
python main.py
```

---

## 📝 License

This project is distributed under the **MIT License**. You are free to use and modify the code without restrictions.

---

🚀 **Thank you for using Google Sheets Auto-Filler!** 🎉

---

# 📊 Google Sheets Auto-Updater

**RU**

**Google Sheets Auto-Updater** — это Python-скрипт, который автоматически проверяет доступ к редактированию таблицы Google Sheets, получает данные из приоритетных ячеек и записывает в первую доступную ячейку заданный текст. Если данные не сохранились, скрипт повторяет попытку до успешной записи.

---

## 🚀 Возможности
- ✅ Автоматически получает данные из указанных ячеек Google Sheets.
- ✅ Проверяет доступ к редактированию таблицы.
- ✅ Записывает в первую доступную ячейку заданный **текст**.
- ✅ Позволяет изменять **ID таблицы** и **ID конкретного листа**.
- ✅ Гибко настраиваемый **порог проверки данных** (например, если текст меньше 3 символов).
- ✅ Обрабатывает **ошибки API** (если API временно недоступен, код ждет и пробует снова).

---

## 🛠️ Установка и настройка

### **1️⃣ Установите зависимости**
```bash
pip install -r requirements.txt
```
```bash
pip install gspread oauth2client
```

### **2️⃣ Создайте учетную запись Google API и скачайте JSON-файл**
1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/).
2. Включите API Google Sheets.
3. Создайте сервисный аккаунт и скачайте JSON-файл с учетными данными.
4. Добавьте email сервисного аккаунта в доступ к Google Sheets (как **Редактор**).

### **3️⃣ Сохраните JSON-файл с учетными данными**
Поместите JSON-файл (например, `credentials.json`) в корневую папку проекта.

### **4️⃣ Настройте переменные в `config.py`**
```python
CREDENTIALS_FILE = 'credentials.json'  # Учетные данные
SPREADSHEET_ID = '12nhlnFIUZBPNyPWrJYKhkdvm-8fPb2CKbaOLUxiOLB0'  # ID Google-таблицы
SHEET_ID = 0  # ID конкретного листа (0 = первый лист)
TEXT = "Фамилия Имя Отчество"  # Что записывать
CHECK_PREFIX = "Фамил"  # Проверяемый префикс (например, "Косья")
PRIORITY_CELLS = ['B3', 'B8', 'B6', 'B12', 'B17']  # Приоритет ячеек
```

---

## 🔄 Как работает скрипт?

1️⃣ **Проверяет доступ** к таблице (читатель или редактор).  
2️⃣ **Получает данные** из ячеек с приоритетом.  
3️⃣ Если **"TEXT" уже записан** в одной из ячеек — **скрипт завершает работу**.  
4️⃣ **Ячейки обрабатываются в порядке приоритета**. Текст записывается в **первую подходящую ячейку**, которая:
   - Либо **пуста**.
   - Либо содержит **CHECK_PREFIX** (например, если `CHECK_PREFIX = "12345"`, то **в ячейку с `12345` текст запишется**, но **не запишется в `123456`**, и запишется в `123`).
5️⃣ Если **после записи осталось CHECK_PREFIX** (например, "Косья") — **дописывает полное значение**.  
6️⃣ Если запись удаляется **после вставки** — пробует следующую доступную ячейку.  

---

## 🏃 Запуск скрипта

```bash
python main.py
```

---

## 📌 Пример работы
```bash
🔹 SPREADSHEET_ID: 12nhlnFIUZBPNyPWrJYKhkdvm-8fPb2CKbaOLUxiOLB0
🔹 SHEET_ID: 0
🔹 TEXT: Иванов Иван Иванович
🔹 CHECK_PREFIX: Иван

🔄 Проверяем доступ...
✅ Доступ к записи есть!
📋 Текущие значения ячеек: {'B3': '', 'B8': '', 'B6': '', 'B12': '', 'B17': ''}
✅ Записали 'Иванов Иван Иванович' в B3
🎉 Полностью записано 'Иванов Иван Иванович' в B3. Остановка.
```

---

## ❗ Возможные ошибки и их решение

### **1️⃣ Ошибка доступа (APIError: 403)**
🔹 **Причина:** Аккаунт не добавлен в список редакторов Google Sheets.  
✅ **Решение:** Добавьте email сервисного аккаунта в **доступ** к Google Sheets.

### **2️⃣ Ошибка "Invalid range" или "Invalid requests"**
🔹 **Причина:** Ошибки в указанных ячейках или недоступность данных.  
✅ **Решение:** Проверьте, что лист и ячейки существуют в таблице.

### **3️⃣ Ошибка "Quota exceeded" (Превышен лимит API)**
🔹 **Причина:** Слишком частые запросы.  
✅ **Решение:** Увеличьте интервал проверки (`time.sleep(1)` → `time.sleep(5)`).

---

## 📝 Лицензия
Этот проект распространяется под лицензией **MIT**. Вы можете использовать и модифицировать код без ограничений.

---

## 👨‍💻 Автор
📌 **Разработчик:** [Ваше имя / GitHub](https://github.com/your-profile)  
📌 **Контакты:** your.email@example.com  

🚀 **Спасибо за использование Google Sheets Auto-Updater!** 🎉


