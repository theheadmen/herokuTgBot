import ftplib
import urllib.request
from io import BytesIO
from PIL import Image
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import datetime

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    chat_id = update.message.chat_id
    update.message.reply_text('Start getting last photo from space...!')
    url = get_image()
    bot.send_photo(chat_id = chat_id, photo=open(url, 'rb'))

def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def get_image():
    ftp = ftplib.FTP("ftp.ntsomz.ru")
    ftp.login("electro", "electro")
    ftp.cwd('ELECTRO_L_2')

    now = datetime.datetime.now()
    now.year
    data = []
    ftp.dir('-t', data.append)
    newfld = str(now.year)
    #data[0].rsplit(' ',1)[1] #year
    year = newfld
    print(newfld)
    ftp.cwd(newfld)

    data = []
    ftp.dir('-t', data.append)
    newfld = data[0].rsplit(' ',1)[1] #month
    month = newfld
    print(newfld)
    ftp.cwd(newfld)

    data = []
    ftp.dir('-t', data.append)
    newfld = data[0].rsplit(' ',1)[1] #day
    day = newfld
    print(newfld)
    ftp.cwd(newfld)

    data = []
    ftp.dir('-t', data.append)
    newfld = data[0].rsplit(' ',1)[1] #time
    time = newfld
    print(newfld)
    ftp.cwd(newfld)

    data = []
    ftp.dir('-t', data.append)
    sub = time + "_RGB"
    file = ""
    for text in data:
        if sub in text:
            file = text
    print(file.rsplit(' ',1)[1])
    filePath = file.rsplit(' ',1)[1]
    imagePath = "ftp://electro:electro@ftp.ntsomz.ru/ELECTRO_L_2/" + year + "/" + month + "/" + day + "/" + time + "/" + filePath  
    #print(imagePath)
    c = ""
    with urllib.request.urlopen(imagePath) as url:
        c = BytesIO(url.read())
    
    img = Image.open(c)
    img.save("img1.png","PNG")
    return("img1.png")
    #img.show() 

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("390817804:AAHODaZ8obpcIR9iQwPbhHvVBJI66vlMOgs")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
