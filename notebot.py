import telebot
import json
TOKEN = ""
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, я бот. Чтобы узнать что я умею введите /help")


@bot.message_handler(commands=['help'])
def send_tutotial(message):
    bot.send_message(message.chat.id, "\nЯ умею записывать заметки.\n/add-добавить заметку\n/list-вывести все заметки\n/clear-очистить все заметки")


@bot.message_handler(commands=['add'])
def add_note(message):
    bot.send_message(message.chat.id, "Напиши заметку")
    bot.register_next_step_handler(message, save_note)

def save_note(message):
    chat_id = message.chat.id
    note_text = message.text
    user_id = str(message.from_user.id)

    try:
        with open("notes.json", "r", encoding="utf-8") as file:
            notes = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        notes = {}

    if user_id not in notes:
        notes[user_id] = []

    notes[user_id].append(note_text)

    with open("notes.json", "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=4)

    bot.send_message(chat_id, f"Заметка сохранена: {note_text}")


@bot.message_handler(commands=['list'])
def list_notes(message):
    user_id = str(message.from_user.id)
    chat_id = message.chat.id

    try:
        with open("notes.json", "r") as file:
            notes = json.load(file)
    except FileNotFoundError:
        notes = {}

    if user_id not in notes or not notes[user_id]:
        bot.send_message(chat_id, "У тебя пока нет ни одной заметки.")
    else:
        note_list = "\n".join(f"• {note}" for note in notes[user_id])
        bot.send_message(chat_id, f"📝 Твои заметки:\n{note_list}")

@bot.message_handler(commands=['clear'])
def clear_notes(message):
    user_id = str(message.from_user.id)
    chat_id = message.chat.id

    try:
        with open("notes.json", "r") as file:
            notes = json.load(file)
    except FileNotFoundError:
        notes = {}

    if user_id in notes:
        notes[user_id] = []  # Очищаем список заметок

        with open("notes.json", "w") as file:
            json.dump(notes, file, indent=4, ensure_ascii=False)

        bot.send_message(chat_id, "Все твои заметки удалены.")
    else:
        bot.send_message(chat_id, "У тебя и так нет заметок.")




bot.polling()
