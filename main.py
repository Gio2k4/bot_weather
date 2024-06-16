from keep_alive import keep_alive
keep_alive()
import telebot
import datetime
import time
import os, sys, re
import requests

API_KEY = '92f483687ed2bd458d8b35ca93ab6bcf'
bot_token = '7349816865:AAHvI-qB_TtKfOdhQyWK1xunoh-TxzM3PVc'
bot = telebot.TeleBot(bot_token)
ADMIN_ID = '5484347837'
processes = []


def TimeStamp():
    now = str(datetime.date.today())
    return now


#Hàm thời tiết
@bot.message_handler(commands=['weather'])
def weather(message):
    city = message.text.split('/weather', 1)[1].strip()
    if not city:
        bot.reply_to(message, 'Vui lòng nhập tên thành phố.')
        return

    try:
        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        )
        data = response.json()
        if data['cod'] == '404':
            bot.reply_to(
                message,
                'Không tìm thấy thông tin thời tiết cho thành phố này.')
        else:
            weather_desc = data['weather'][0]['description']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            bot.reply_to(
                message,
                f'Thời tiết tại {city}:\nMô tả: {weather_desc}\nNhiệt độ: {temp}°C\nĐộ ẩm: {humidity}%\nTốc độ gió: {wind_speed} m/s'
            )
    except requests.exceptions.RequestException as e:
        bot.reply_to(message, 'Đã xảy ra lỗi khi truy xuất dữ liệu thời tiết.')


@bot.message_handler(commands=['hdsd'])
def help(message):
    help_text = '''
Danh sách lệnh:

- /weather + tỉnh thành: xem thời tiết ở tỉnh thành cần xem

'''
    bot.reply_to(message, help_text)


# status
@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return
    process_count = len(processes)
    bot.reply_to(message, f'Số quy trình đang chạy: {process_count}.')


# khoir dong lai bot
@bot.message_handler(commands=['restart'])
def restart(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return
    bot.reply_to(message, 'Bot sẽ được khởi động lại trong giây lát...')
    time.sleep(2)
    python = sys.executable
    os.execl(python, python, *sys.argv)


# stop chuongw trinhf
@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id
    if str(user_id) != ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return
    bot.reply_to(message, 'Bot sẽ dừng lại trong giây lát...')
    time.sleep(2)
    bot.stop_polling()


bot.polling()
