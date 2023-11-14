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

is_swapping = False



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
        if current_user in queue:
            if current_user.id == queue[0].id:
                await update.message.reply_text("ВЫ ПЕРВЫЙ В ОЧЕРЕДИ")
            else:
                await update.message.reply_text("УВЫ")
    else:
        await update.message.reply_text('Очередь пуста.')

async def swap_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if user in queue:
        is_swapping = True
        current_queue = [f'{i+1}. {user.first_name} - @{user.username}' for i, user in enumerate(queue)]
        await update.message.reply_text(type(current_queue[0]).__name__)
    else:
        await update.message.reply_text('Вы не в очереди.')
    reply_keyboard =   [current_queue]#[['👉Вступить в очередь👉', '👈Покинуть очередь👈'], ['💀Увидеть очередь и умереть💀']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(f'С кем бы вы хотели поменяться?', reply_markup=markup)

TEXT_HANDLERS = {
    '👉Вступить в очередь👉': enqueue,
    '👈Покинуть очередь👈': dequeue,
    '💀Увидеть очередь и умереть💀': status,
    '👉👈Поменяться местами👉👈' : swap_request
}

commands = list(TEXT_HANDLERS.keys())



async def user_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.first_name
    await update.message.reply_text(f'Дарова, {username}! Чего бы вы хотели?')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    handler = TEXT_HANDLERS.get(text)

    if handler:
        await handler(update, context)
    else:
        if (text == "Кто нахуй?" and not is_swapping):
            await update.message.reply_text('Я нахуй!')
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Шо я не понял?")


# Команда start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.first_name

    reply_keyboard = [[commands[0], commands[1]], [commands[2]], [commands[3]]] #[['👉Вступить в очередь👉', '👈Покинуть очередь👈'], ['💀Увидеть очередь и умереть💀']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

    await update.message.reply_text(f'Привет, {username}! Чего бы вы хотели?', reply_markup=markup)


if __name__ == '__main__':
    application = ApplicationBuilder().token('6878650923:AAGz0mV5QlnzC2WtClIldVx66fo4qwm6VXI').build()

    #nick = 

    start_handler = CommandHandler('start', start)

    enqueue_handler = CommandHandler('enqueue', enqueue)
    dequeue_handler = CommandHandler('dequeue', dequeue)
    
    status_handler = CommandHandler('status', status)

    user_handler = MessageHandler(filters.USER & (~filters.COMMAND), user_check)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(enqueue_handler)
    application.add_handler(dequeue_handler)
    application.add_handler(status_handler)
    application.add_handler(echo_handler)
    application.add_handler(unknown_handler)

    application.run_polling()