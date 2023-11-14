import logging
from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackContext
from collections import deque

import random

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


from collections import deque

# Очередь клиентов
queue = deque()

# никнейм клиента



# Встать в очередь
async def enqueue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if user not in queue:
        queue.append(user)
        await update.message.reply_text(f'Вы встали в очередь.')
    else:
        await update.message.reply_text('Вы уже в очереди.')

# Покинуть очередь
async def dequeue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    if user in queue:
        queue.remove(user)
        await update.message.reply_text('Вы покинули очередь.')
    else:
        await update.message.reply_text('Вы не в очереди.')

# Текущее состояние очереди
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_user = update.message.from_user
    if queue:
        current_queue = [f'{i+1}. {user.first_name} - @{user.username}' for i, user in enumerate(queue)]
        await update.message.reply_text('\n'.join(current_queue))
        if current_user.id == queue[0].id:
            await update.message.reply_text("ВЫ ПЕРВЫЙ В ОЧЕРЕДИ")
        else:
            await update.message.reply_text("УВЫ")
    else:
        await update.message.reply_text('Очередь пуста.')

TEXT_HANDLERS = {
    'Вступить в очередь': enqueue,
    'Покинуть очередь': dequeue,
    'Статус очереди': status
}


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    handler = TEXT_HANDLERS.get(text)

    if handler:
        await handler(update, context)
    else:
        if text == "Кто нахуй?":
            await update.message.reply_text('Я нахуй!')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")



# Команда start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.first_name

    reply_keyboard = [['Вступить в очередь', 'Покинуть очередь'], ['Статус очереди']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    await update.message.reply_text(f'Привет, {username}! Чего бы вы хотели?', reply_markup=markup)


if __name__ == '__main__':
    application = ApplicationBuilder().token('6878650923:AAGz0mV5QlnzC2WtClIldVx66fo4qwm6VXI').build()

    #nick = 

    start_handler = CommandHandler('start', start)

    enqueue_handler = CommandHandler('enqueue', enqueue)
    dequeue_handler = CommandHandler('dequeue', dequeue)
    
    status_handler = CommandHandler('status', status)


    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(enqueue_handler)
    application.add_handler(dequeue_handler)
    application.add_handler(status_handler)
    application.add_handler(echo_handler)
    application.add_handler(unknown_handler)

    application.run_polling()