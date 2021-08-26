import logging
from telegram.ext import *
from telegram import *
import responses

API_KEY = 'YOUR_API_KEY'
bot = None
# Set up the logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')


def high_p_command(update, context):
    """
    Handles the high protein command returns list sorted by protein percentage.
    """
    response = responses.high('p')
    update.message.reply_text(response)


def high_f_command(update, context):
    """
    Handles the fat protein command returns list sorted by fat percentage.
    """
    response = responses.high('f')
    update.message.reply_text(response)


def high_c_command(update, context):
    """
    Handles the high carbohydrates command returns list sorted by carbohydrates percentage.
    """
    response = responses.high('c')
    update.message.reply_text(response)


def high_fp_command(update, context):
    """
    Handles the high fat and protein command returns list sorted by fat and protein percentage.
    """

    response = responses.high('fp')
    update.message.reply_text(response)


def high_cf_command(update, context):
    """
    Handles the high carbohydrates and fat command returns list sorted by carbohydrates and fat percentage.
    """
    response = responses.high('cf')
    update.message.reply_text(response)


def high_cp_command(update, context):
    """
    Handles the high carbohydrates and protein command returns list sorted by carbohydrates and protein percentage.
    """
    response = responses.high('cp')
    update.message.reply_text(response)


def help_command(update, context):
    """
    Handles the help command returns list of all possible commands with a short explanation. \n
    """
    update.message.reply_text('you can type a name of food item and we will respond with the nutritive composition of '
                              'it and a graph or you can use the commands.\n\n here\'s all the commands :\n'
                              '/high_p will return list of all the food items by their proteins percentage.\n'
                              '/high_c will return list of all the food items by their carbohydrates percentage.\n'
                              '/high_f will return list of all the food items by their fat percentage.\n'
                              '/high_cf will return list of all the food items by their carbohydrates and fat '
                              'percentage.\n/high_cp will return list of all the food items by their carbohydrates '
                              'and proteins percentage.\n '
                              '/high_fp will return list of all the food items by their fat and proteins percentage.')


def handle_message(update, context):
    """
    Handles the messages expecting a food name returns graph image of nutritive composition.
    """
    text = str(update.message.text)
    logging.info(f'User ({update.message.chat.id}) says: {text}')
    response = responses.get_item(text)
    if response != 'I didn\'t understand what you wrote.':
        bot.send_photo(chat_id=update.effective_chat.id, photo=open('img.png', 'rb'), caption=response)
    else:
        bot.sendMessage(chat_id=update.effective_chat.id, text=response)


def error(update, context):
    logging.error(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    bot = Bot(API_KEY)
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('high_p', high_p_command))
    dp.add_handler(CommandHandler('high_c', high_c_command))
    dp.add_handler(CommandHandler('high_f', high_f_command))
    dp.add_handler(CommandHandler('high_cf', high_cf_command))
    dp.add_handler(CommandHandler('high_cp', high_cp_command))
    dp.add_handler(CommandHandler('high_fp', high_fp_command))
    dp.add_handler(CommandHandler('help', help_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()
