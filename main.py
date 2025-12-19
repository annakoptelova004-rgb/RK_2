import telebot
from telebot import types
from datetime import datetime

# Мой токен
bot = telebot.TeleBot("7605077620:AAHH-OoZEYHOKr6NexqfNmnh-CbF47YHgpY")

# Словарь для хранения данных пользователей
user_data = {}

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Услуги")
    btn2 = types.KeyboardButton("Мастера")
    btn3 = types.KeyboardButton("Записаться")
    btn4 = types.KeyboardButton("Контакты")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(message.chat.id, 
                    "Добро пожаловать в салон красоты 'Элегант'! \n\n"
                    "Выберите действие:", 
                    reply_markup=markup)

# Кнопка "Услуги"
@bot.message_handler(func=lambda message: message.text == "Услуги")
def show_services(message):
    services = """*Наши услуги и цены:*

• *Стрижка женская* - 1500 руб.
• *Стрижка мужская* - 800 руб.
• *Окрашивание* - от 2500 руб.
• *Маникюр* - 1200 руб.
• *Педикюр* - 1500 руб.
• *Макияж* - 2000 руб.

*Записаться:* нажмите кнопку 'Записаться'"""
    
    bot.send_message(message.chat.id, services, parse_mode='Markdown')

# Кнопка "Мастера"
@bot.message_handler(func=lambda message: message.text == "Мастера")
def show_masters(message):
    masters = """*Наша команда мастеров:*

*Анна Иванова* - топ-стилист
• Стрижки, окрашивание
• Стаж: 8 лет

*Мария Петрова* - мастер маникюра
• Маникюр, педикюр, дизайн
• Стаж: 5 лет

*Иван Сидоров* - барбер
• Мужские стрижки, бритье
• Стаж: 6 лет

*Записаться к мастеру:* нажмите 'Записаться'"""
    
    bot.send_message(message.chat.id, masters, parse_mode='Markdown')

# Кнопка "Записаться"
@bot.message_handler(func=lambda message: message.text == "Записаться")
def start_booking(message):
    markup = types.ReplyKeyboardRemove()
    msg = bot.send_message(message.chat.id, 
                          "*Запись на услугу*\n\n"
                          "Введите ваше имя:",
                          parse_mode='Markdown',
                          reply_markup=markup)
    bot.register_next_step_handler(msg, process_name)

def process_name(message):
    name = message.text
    user_data[message.chat.id] = {'name': name}
    
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Стрижка женская", "Стрижка мужская", "Окрашивание", "Маникюр", "Педикюр", "Макияж")
    
    msg = bot.send_message(message.chat.id, 
                          f"Приятно познакомиться, {name}!\nВыберите услугу:",
                          reply_markup=markup)
    bot.register_next_step_handler(msg, process_service)

def process_service(message):
    service = message.text
    # Сохраняем услугу в данных пользователя
    user_data[message.chat.id]['service'] = service
    
    markup = types.ReplyKeyboardRemove()
    msg = bot.send_message(message.chat.id, 
                          f"Вы выбрали: {service}\nНа какую дату хотите записаться? (например: 08.11.2025)",
                          reply_markup=markup)
    bot.register_next_step_handler(msg, process_date)

def process_date(message):
    try:
        date_str = message.text
        
        # Проверяем формат даты
        try:
            appointment_date = datetime.strptime(date_str, '%d.%m.%Y').date()
        except ValueError:
            bot.send_message(message.chat.id, "❌ Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ (например: 10.11.2025)")
            return

        # Получаем данные пользователя
        user_info = user_data.get(message.chat.id, {})
        name = user_info.get('name', 'Неизвестно')
        service = user_info.get('service', 'Неизвестно')
        
        # Отправляем подтверждение
        confirmation_text = (
            f"✅ *Запись подтверждена!*\n\n"
            f"*Имя:* {name}\n"
            f"*Услуга:* {service}\n"
            f"*Дата:* {date_str}\n\n"
            f"Ждем вас в салоне 'Элегант'!"
        )
        
        bot.send_message(message.chat.id, confirmation_text, parse_mode='Markdown')
        
        # Очищаем данные пользователя
        if message.chat.id in user_data:
            del user_data[message.chat.id]
            
        # Возвращаем главное меню
        send_welcome(message)
        
    except Exception as e:
        print(f"Ошибка: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка при обработке записи. Пожалуйста, попробуйте снова.")

# Кнопка "Контакты"
@bot.message_handler(func=lambda message: message.text == "Контакты")
def show_contacts(message):
    contacts = """*Наши контакты:*

*Адрес:* ул. 2-я Бауманская 5,стр.4
*Телефон:* +7 (495) 123-45-67
*Режим работы:* 9:00 - 21:00

*Как добраться:* [Открыть карту](https://yandex.ru/maps/org/moskovskiy_gosudarstvenny_tekhnicheskiy_universitet_imeni_n_e_baumana/1207959729/)"""
    
    bot.send_message(message.chat.id, contacts, parse_mode='Markdown')

# Запуск бота
print("Бот салона красоты запущен...")
bot.polling()