[![wakatime](https://wakatime.com/badge/github/noinsts/klen4k-bot.svg)](https://wakatime.com/badge/github/noinsts/klen4k-bot)

# klen4k-bot 🤖

**klen4k-bot** — це багатофункціональний Discord-бот, названий в честь мого друга Леоніда, який дав мені елінти в Майнкрафті. Створений за допомогою бібліотеки `discord.py`. Він допомагає у модерації, керуванні ролями, голосовими каналами та іншими функціями сервера.

## ⚙ Встановлення та налаштування

### 1️⃣ Клонування репозиторію
```bash
git clone https://github.com/noinsts/klen4k-bot.git
cd klen4k-bot
```

### 2️⃣ Встановлення залежностей
Переконайтеся, що у вас встановлений Python 3.7 або вище. Потім виконайте команду:
```bash
pip install -r requirements.txt
```

### 3️⃣ Налаштування `.env`
Створіть файл `.env` у кореневій директорії та додайте наступне:
```ini
TOKEN=Ваш_токен_бота
API_KEY=Ваш_токен_стім_АПІ
PASSWORD=Пароль
WEATHER_API=Ваш_openweather_ключ
CLIENT_REDDIT_API = Ваш_кліет_айді_реддіту
SECRET_REDDIT_API = Ваш_секретний_токен_реддіту
```
Замініть `Ваш_токен_бота` на ваш реальний токен бота з [Discord Developer Portal](https://discord.com/developers/applications).

Замість `Ваш_токен_стім_АПІ` на ваш реальний токен з [Steam](https://steamcommunity.com/dev/apikey).

Замість `Пароль` придумайте пароль для видалення бд балансів користувачів (вводити в лапках, int або float)

Замість `Ваш_openweather_ключ` на ваш реальний токен з [OpenWeather](https://openweathermap.org/).

Замість `Ваш_кліет_айді_реддіту` на ваш реальний кліент айді з [RedditApps](https://www.reddit.com/prefs/apps)

Замість `Ваш_секретний_токен_реддіту` на ваш реальний токен реддіт з [RedditApps](https://www.reddit.com/prefs/apps)

### 4️⃣ Запуск бота
```bash
python main.py
```

## 🛠 Команди

### 🎭 Ролі (`cogs/roles.py`)
- **`.role add/remove <role> [@member]`** – Додає/видаляє роль учаснику.

### 🔨 Модерація (`cogs/moderation.py`)
- **`.timeout @member <time_in_minutes> [reason]`** – Видає тайм-аут учаснику.
- **`.nickname @member [new_nick]`** – Змінює нікнейм (якщо `new_nick` не вказано, скидає нік).
- **`.vacban @member [reason]`** - блокує користувача на сервері
- **`.mute @member`** - мутить користувача в войсі
- **`.unmute @member`** - розмучує користувача в войсі
- **`.deafen @member`** - заглушає користувача в войсі
- **`.undeafen @member`** - розглушає користувача в войсі
- **`.poll (action), (time), (member), (reason)`** - створення голосування для виконання дій над користувачем

### 🔊 Голосові канали (`cogs/voice.py`)
- **`.afk @member`** - відправляє вказану людину в войс `cfg.AFK_ID`
- **`.roulette`** - кікає рандомну людину з вашого войсу
- **`.private @member`** - відправляє вас та вказану людину в окремий войс
- **`.vlock`** – Закриває доступ до голосового каналу для `@everyone`.
- **`.vunlock`** – Відкриває доступ до голосового каналу.
- **`.vc_slots`** - змінює кількість слотів у вашому войсі

### 💬 Чат (`cogs/voice.py`)
- **`.userinfo @member`** - видає інформацію про учасника
- **`.choice [ask]`** - відповідає на запитання так, ні або можливо
- **`.who [ask]`** - обирає випадкову людину з сервера

### 👥 Teams (`cogs/teams.py`)
- **`.teams_create`** - розподіляє учасників войса на дві команди (працює, якщо у войсі 4 людини)
- **`.clear_teams`** - прибирає в учасників сервера ролі `cfg.ROLE_1_ID`, `cfg.ROLE_2_ID`
- **`.teammerge`** - переміщає команди в `cfg.FULL_STACK`
- **`.teamsplit`** - роз'єднує команди по різних войса (team1 в `cfg.ROLE_A_ID`, team2 в `cfg.ROLE_B_ID`)

### 📆 Календар (`cogs/cal.py`)
- **`.calendar type:year/month, year, month`** - виводить красивий календар

### 🎂 Birthdays (`cogs/birthdays.py`)
- **`.add_birthday (date: YYYY-MM-DD), @member or None`** - Записує день народження користувача в базу даних.
- **`.update_birthday (date: YYYY-MM-DD), @member or None`** - Оновлює день народження користувача в базі даних.
- **`.remove_birthday (@member or None)`** - Видаляє день народження користувача з бази даних.
- **`.birthday (@member or None)`** - Виводить день народження користувача.
- **`.birthday_list`** - Виводить список всіх днів народження, збережених у базі даних.
- **`.in_my_day (@member or None)`** - Виводить список користувачів, у яких день народження збігається з днем народження вказаного користувача.
- **`.come_birthday`** - Виводить список найближчих днів народження (поки не працює).

### 💰 Balance (`cogs/balance.py`)
- **`.change_balance ( only admin amount: int), @member or None`** - Змінює баланс користувача на вказану суму. Якщо користувача не вказано, змінює баланс автора команди. (Адміністратор)
- **`.balance (@member or None)`** - Виводить баланс вказаного користувача або автора команди.
- **`.balance_tier_list`** - показує список багатих людей сервера
- **`.balance_privacy`** - змінює `True/False` демонстрацію вашого балансу в списку лідерів
- **`.exchange (from) (to) (money)`** - обмін валют. Працює тільки з `USD/EUR/UAH`.

### 📢 Автоматичні податки (`cogs/taxes.py`)
- **`.taxes`** - показує список податків та їх вартість
- **`.toggle_taxes (only admin)`** - вмикає або вимикає податки
- **`on_voice_state_update`** - Коли користувач приєднується до голосового каналу, з його балансу знімається податок (`join_voice`). Якщо логування увімкнене, запис надсилається в лог-канал.
- **`.change_tax (only admin action: str, amount: int)`** - Змінює податок для вказаної дії (наприклад, `join_voice`). (Адміністратор)

### ☀️ Погода (`cogs/weather.py`)
- **`.weather (city)`** - показує: температуру, вологість, опис погоди. Змінює рамку embed до погоди
- **`.weather (city)`** – показує: температуру, вологість, опис погоди. Змінює рамку embed до погоди.  
- **`.set_location or add_location (city) (country)`** – зберігає ваше місто та країну в базі, щоб бот знав, звідки брати погоду.  
- **`.change_location (city) (country)`** – змінює ваше місто та країну в базі, якщо ви переїхали або зробили помилку.  
- **`.del_location or delete_location`** – видаляє ваше місто та країну з бази, якщо ви більше не хочете зберігати його.  
- **`.add_weather_advice (positive/negative) (advice)`** - вказуєте, що ви б робили б в позитивну/негативну погоду
- **`.personalize_advice`** - бот на основі ваших побажань та погоди за вікном накидує вам пораду

### 📱 Смартфони (`cogs/phones.py`)
- **`.add_phone (brand) (model)`** - додає ваш телефон до бази даних.
- **`.edit_phone (brand) (model)`** - змінює інформацію про ваш телефон в базі (якщо він є).
- **`.delete_phone`** - видаляє ваш телефон з бд (якщо він є).
- **`.phone (member or None)`** - пише інформацію про смартфон людини (за замовчуванням про ваш).

### 🎨 Колір (`cogs/color.py`)
- **`.add_color (color)`** - додає ваш улюблений колір
- **`.edit_color (color)`** - змінює ваш улюблений колір
- **`.delete_color`** - видаляє колір з бд

### 🤖 Reddit (`cogs/reddit.py`)
- **`.top (subreddit_name)`** - видає топ 1 пост з вказаного subreddit_name
- **`.meme`** - видає рандомний мем з r/ukr_memes

### ☕ Coffee (`cogs/coffee.py`)
- **`.coffee_menu`** - Відображає меню кав 

## 📝 Логування

### 🔊 Голосові канали (`cogs/logs.py`)
- контролює стан голосового каналу, та коли учасник сервера заходить/виходить/переміщується, бот повідомляє про це в `cfg.LOG_CHANNEL_ID`, якщо в database.db -> show_logs -> voice_logs == 1


## 🛡 Ліцензія  
Цей проєкт ліцензовано під [MIT License](./LICENSE).

## ✨ Автор
**[@noinsts](https://github.com/noinsts)** – автор і розробник цього бота.
