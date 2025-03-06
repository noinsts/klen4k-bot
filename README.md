# klen4k-bot 🤖

**klen4k-bot** — це багатофункціональний Discord-бот, створений за допомогою бібліотеки `discord.py`. Він допомагає у модерації, керуванні ролями, голосовими каналами та іншими функціями сервера.

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
```
Замініть `Ваш_токен_бота` на ваш реальний токен бота з [Discord Developer Portal](https://discord.com/developers/applications).

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

### 🔊 Голосові канали (`cogs/voice.py`)
- **`.afk @member`** - відправляє вказану людину в войс `cfg.AFK_ID`
- **`.roulette`** - кікає рандомну людину з вашого войсу
- **`.private @member`** - відправляє вас та вказану людину в окремий войс
- **`.vlock`** – Закриває доступ до голосового каналу для `@everyone`.
- **`.vunlock`** – Відкриває доступ до голосового каналу.

### 💬 Чат (`cogs/voice.py`)
- **`.userinfo @member`** - видає інформацію про учасника
- **`.choice [ask]`** - відповідає на запитання так, ні або можливо
- **`.who [ask]`** - обирає рандомну людину з серверу

### 👥 Teams (`cogs/teams.py`)
- **`.teams_create`** - розподіляє учасників войсу на дві команди (працює, якщо у войсі 4 людини)
- **`.clear_teams`** - прибирає в учасників серверу ролі `cfg.ROLE_1_ID`, `cfg.ROLE_2_ID`
- **`.teammerge`** - переміщає команди в `cfg.FULL_STACK`
- **`.teamsplit`** - роз'єднує команди по різних войсах (team1 в `cfg.ROLE_A_ID`, team2 в `cfg.ROLE_B_ID`)

## 📝 Логування

### 🔊 Голосові канали (`cogs/logs.py`)
- контролить стан голосового каналу, та коли учасник серверу заходить/виходить/переміщується, бот повідомляє про це в `cfg.LOG_CHANNEL_ID` 


## 📜 Ліцензія
Цей проект розповсюджується без ліцензії.

## ✨ Автор
**[@noinsts](https://github.com/noinsts)** – автор і розробник цього бота.
